import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO

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
        c.execute("""
            INSERT INTO opportunities (type, organization, opportunity, address, price, salary, duration, deadline, contact, email) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

def save_to_xlsx(entries):
    df = pd.DataFrame(entries)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Opportunities')
        writer.save()
    return output.getvalue()

def save_to_csv(entries):
    df = pd.DataFrame(entries)
    return df.to_csv(index=False).encode('utf-8')

# ----------------------------
# STREAMLIT UI FOR ADMIN
# ----------------------------
st.set_page_config(page_title="🔐 Admin Opportunity DB", layout="wide")
st.title("🔐 Admin Opportunity Dashboard")
st.caption("Admins can add, edit, and generate TLDRs")

entries = load_entries()

# ----------------------------
# Create Layout with Columns
# ----------------------------
col1, col2 = st.columns([2, 1])  # Left column (Database) is 2x the width of the right column (Form)

# ------------- LEFT SIDE: DATABASE LIST -------------------
with col1:
    st.subheader("📊 Stored Opportunities")
    if entries:
        df = pd.DataFrame(entries).drop(columns=["id"])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # TLDR Export for Each Item and All Items
    st.subheader("📝 Export TLDR for Individual Opportunities")
    for entry in entries:
        tldr = generate_tldr_text(entry)
        st.download_button(
            label=f"📥 Download TLDR for {entry['Opportunity']}",
            data=tldr,
            file_name=f"{entry['Opportunity']}_tldr.txt",
            mime="text/plain",
            key=f"tldr_{entry['id']}"  # Add a unique key for each button
        )

    # TLDR Export for All Opportunities
    st.subheader("📝 Export TLDR for All Opportunities")
    tldr_output = "\n\n".join([generate_tldr_text(e) for e in entries])
    st.download_button(
        label="📥 Download All TLDRs (txt)",
        data=tldr_output,
        file_name="all_opportunities_tldr.txt",
        mime="text/plain",
        key="all_tldr_txt"  # Unique key for the "All TLDRs" button
    )
    st.download_button(
        label="📥 Download All Opportunities (CSV)",
        data=save_to_csv(entries),
        file_name="all_opportunities.csv",
        mime="text/csv",
        key="all_csv"  # Unique key for the CSV button
    )
    st.download_button(
        label="📥 Download All Opportunities (XLSX)",
        data=save_to_xlsx(entries),
        file_name="all_opportunities.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="all_xlsx"  # Unique key for the XLSX button
    )


    else:
        st.info("No entries yet. Add one above!")

# ------------- RIGHT SIDE: FORM -------------------
with col2:
    st.subheader("✏️ Add or Edit Opportunity")
    selected_id = st.selectbox("Select an opportunity to edit", ["New Entry"] + [f"{e['id']}: {e['Opportunity']}" for e in entries])
    
    editing_entry = {
        "id": None, "Type": "Competition", "Organization": "", "Opportunity": "", "Address": "", "Price": "",
        "Salary": "", "Duration": "", "Deadline": "", "Contact": "", "Email": ""
    }
    if selected_id != "New Entry":
        selected_id = int(selected_id.split(":")[0])
        editing_entry = next((e for e in entries if e["id"] == selected_id), editing_entry)

    with st.form("opportunity_form"):
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
                st.stop()
