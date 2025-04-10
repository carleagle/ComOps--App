import streamlit as st
import sqlite3
import pandas as pd

# ----------------------------
# DATABASE SETUP
# ----------------------------
conn = sqlite3.connect("opportunities.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    organization TEXT,
    opportunity TEXT,
    address TEXT,
    price TEXT,
    salary TEXT,
    duration TEXT,
    deadline TEXT,
    contact TEXT,
    email TEXT
)''')
conn.commit()

# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def save_entry_to_db(entry):
    if entry.get("id") is not None:
        # Update existing entry
        c.execute("""
            UPDATE opportunities SET
                type=?, organization=?, opportunity=?, address=?, price=?,
                salary=?, duration=?, deadline=?, contact=?, email=?
            WHERE id=?
        """, (
            entry["Type"], entry["Organization"], entry["Opportunity"], entry["Address"], entry["Price"],
            entry["Salary"], entry["Duration"], entry["Deadline"], entry["Contact"], entry["Email"], entry["id"]
        ))
    else:
        # Insert new entry (exclude "id")
        c.execute("""
            INSERT INTO opportunities (
                type, organization, opportunity, address, price,
                salary, duration, deadline, contact, email
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry["Type"], entry["Organization"], entry["Opportunity"], entry["Address"], entry["Price"],
            entry["Salary"], entry["Duration"], entry["Deadline"], entry["Contact"], entry["Email"]
        ))
    conn.commit()

def load_entries():
    c.execute("SELECT * FROM opportunities")
    rows = c.fetchall()
    return [
        {
            "id": row[0], "Type": row[1], "Organization": row[2], "Opportunity": row[3], "Address": row[4],
            "Price": row[5], "Salary": row[6], "Duration": row[7], "Deadline": row[8],
            "Contact": row[9], "Email": row[10]
        } for row in rows
    ]

def generate_tldr_text(entry):
    return f"""📌 {entry['Opportunity']} ({entry['Type']})\n🏢 {entry['Organization']}\n📍 {entry['Address']}\n💰 Price: {entry['Price'] or 'N/A'} | Salary: {entry['Salary'] or 'N/A'}\n🕒 Duration: {entry['Duration']}\n📅 Deadline: {entry['Deadline']}\n📞 {entry['Contact']} | 📧 {entry['Email']}\n"""

# ----------------------------
# STREAMLIT UI FOR ADMIN
# ----------------------------
st.set_page_config(page_title="🔐 Admin Opportunity DB", layout="centered")
st.title("🔐 Admin Opportunity Dashboard")
st.caption("Admins can add, edit, and generate TLDRs")

entries = load_entries()

# Selection for editing
st.subheader("✏️ Edit Existing Entry")
selected_id = st.selectbox("Select an opportunity to edit", ["New Entry"] + [f"{e['id']}: {e['Opportunity']}" for e in entries])

editing_entry = {
    "id": None, "Type": "Competition", "Organization": "", "Opportunity": "", "Address": "", "Price": "",
    "Salary": "", "Duration": "", "Deadline": "", "Contact": "", "Email": ""
}
if selected_id != "New Entry":
    selected_id = int(selected_id.split(":")[0])
    editing_entry = next((e for e in entries if e["id"] == selected_id), editing_entry)

with st.form("opportunity_form"):
    st.subheader("➕ Add or Edit Opportunity")
    col1, col2 = st.columns(2)
    with col1:
        opportunity_type = st.selectbox("Type", ["Competition", "OJT", "Job Opportunity", "Others"], index=["Competition", "OJT", "Job Opportunity", "Others"].index(editing_entry["Type"]))
        organization = st.text_input("Organization", value=editing_entry["Organization"])
        opportunity = st.text_input("Opportunity Title", value=editing_entry["Opportunity"])
        address = st.text_input("Address", value=editing_entry["Address"])
        price = st.text_input("Price (if any)", value=editing_entry["Price"])
    with col2:
        salary = st.text_input("Salary Expectation", value=editing_entry["Salary"])
        duration = st.text_input("Duration", value=editing_entry["Duration"])
        deadline = st.text_input("Registration Deadline", value=editing_entry["Deadline"])
        contact = st.text_input("Contact Number", value=editing_entry["Contact"])
        email = st.text_input("Email Address", value=editing_entry["Email"])

    submitted = st.form_submit_button("Save Entry")
    if submitted:
        if not opportunity or not organization:
            st.error("Please fill in the required fields.")
        else:
            entry = {
                "id": editing_entry["id"],
                "Type": opportunity_type, "Organization": organization, "Opportunity": opportunity,
                "Address": address, "Price": price, "Salary": salary, "Duration": duration,
                "Deadline": deadline, "Contact": contact, "Email": email
            }
            save_entry_to_db(entry)
            st.success("✅ Entry saved!")
            st.experimental_rerun()
 
# Show database
entries = load_entries()
if entries:
    st.subheader("📊 Stored Opportunities")
    st.dataframe(pd.DataFrame(entries).drop(columns=["id"]), use_container_width=True, hide_index=True)

    # TLDR Export
    st.subheader("📝 Export TLDR")
    tldr_output = "\n\n".join([generate_tldr_text(e) for e in entries])
    st.download_button("📥 Download TLDR (txt)", data=tldr_output, file_name="opportunities_tldr.txt")
else:
    st.info("No entries yet. Add one above!")