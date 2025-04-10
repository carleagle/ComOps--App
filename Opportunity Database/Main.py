import streamlit as st
import sqlite3

# --- DB SETUP ---
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

def save_entry(entry):
    c.execute("""
        INSERT INTO opportunities (type, organization, opportunity, address, price, salary, duration, deadline, contact, email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple(entry.values()))
    conn.commit()

# --- UI ---
st.set_page_config(page_title="🛠️ Edit Opportunities", layout="centered")
st.title("🛠️ Admin: Add New Opportunity")

with st.form("editor_form"):
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

    if st.form_submit_button("Save Entry"):
        if not opportunity or not organization:
            st.error("❗ Required fields missing.")
        else:
            entry = {
                "Type": opportunity_type, "Organization": organization, "Opportunity": opportunity,
                "Address": address, "Price": price, "Salary": salary, "Duration": duration,
                "Deadline": deadline, "Contact": contact, "Email": email
            }
            save_entry(entry)
            st.success("✅ Entry saved successfully!")
