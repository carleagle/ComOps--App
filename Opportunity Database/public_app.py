import streamlit as st
import pandas as pd
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

# ----------------------------
# LOAD ENTRIES FUNCTION
# ----------------------------
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

# ----------------------------
# STREAMLIT UI FOR PUBLIC VIEWER
# ----------------------------
st.set_page_config(page_title="🌍 Public Opportunity DB", layout="centered")
st.title("🌍 Public Opportunity Database")
st.caption("View posted competitions, OJTs, and job listings")

entries = load_entries()
if entries:
    st.dataframe(pd.DataFrame(entries).drop(columns=["id"]), use_container_width=True, hide_index=True)
else:
    st.info("No entries available yet.")
