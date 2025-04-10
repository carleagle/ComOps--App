import streamlit as st
import sqlite3

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

def save_entry_to_db(entry):
    c.execute("""
        INSERT INTO opportunities (type, organization, opportunity, address, price, salary, duration, deadline, contact, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple(entry.values()))
    conn.commit()

def load_entries():
    c.execute("SELECT * FROM opportunities")
    rows = c.fetchall()
    return [
        {
            "Type": row[1], "Organization": row[2], "Opportunity": row[3], "Address": row[4],
            "Price": row[5], "Salary": row[6], "Duration": row[7], "Deadline": row[8],
            "Contact": row[9], "Email": row[10]
        } for row in rows
    ]

# ----------------------------
# STREAMLIT UI
# ----------------------------
st.set_page_config(page_title="📋 Opportunity DB", layout="centered")
st.title("📋 Opportunity Database")
st.caption("Manage competitions, internships, jobs, and more!")

with st.form("opportunity_form"):
    st.subheader("➕ Add New Opportunity")
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
                "Type": opportunity_type, "Organization": organization, "Opportunity": opportunity,
                "Address": address, "Price": price, "Salary": salary, "Duration": duration,
                "Deadline": deadline, "Contact": contact, "Email": email
            }
            save_entry_to_db(entry)
            st.success("✅ Entry saved!")

entries = load_entries()
if entries:
    st.subheader("📊 Stored Opportunities")
    st.dataframe(entries, use_container_width=True, hide_index=True)
else:
    st.info("No entries yet. Add one above!")