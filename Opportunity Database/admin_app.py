import streamlit as st
import sqlite3
import pandas as pd

# ----------------------------
# DATABASE SETUP
# ----------------------------
conn = sqlite3.connect("opportunities.db", check_same_thread=False)
c = conn.cursor()

# Create table if it doesn't exist already
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
    )
''')
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

# ----------------------------
# STREAMLIT UI
# ----------------------------
st.set_page_config(page_title="🔐 Admin Opportunity DB", layout="wide")
st.title("🔐 Admin Opportunity Dashboard")
st.caption("Admins can add and view opportunities")

entries = load_entries()

# Selection for adding new entries
st.subheader("✏️ Add New Opportunity")
with st.form("opportunity_form"):
    st.subheader("➕ Add Opportunity")
    col1, col2 = st.columns(2)
    with col1:
        opportunity_type = st.selectbox("Type", ["Competition", "OJT", "Job Opportunity", "Others"])
        organization = st.text_input("Organization")
        opportunity = st.text_input("Opportunity Title")
        address = st.text_input("Address")
        price = st.text_input("Price (if any)")
    with col2:
        salary = st.text_input("Salary Expectation")
        duration = st.text_input("Duration")
        deadline = st.text_input("Registration Deadline")
        contact = st.text_input("Contact Number")
        email = st.text_input("Email Address")

    submitted = st.form_submit_button("Save Entry")
    if submitted:
        if not opportunity or not organization:
            st.error("Please fill in the required fields.")
        else:
            entry = {
                "id": None,
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
    df = pd.DataFrame(entries).drop(columns=["id"])
    
    # Creating a column for the download button per row
    for idx, row in df.iterrows():
        with st.expander(f"Opportunity {row['Opportunity']}"):
            # Generate the TLDR text for the selected row
            tldr_text = generate_tldr_text(row)
            st.download_button(
                label="📥 Download TLDR", 
                data=tldr_text, 
                file_name=f"{row['Opportunity']}_tldr.txt"
            )

else:
    st.info("No entries yet. Add one above!")
