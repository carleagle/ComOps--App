import streamlit as st
import sqlite3

# --- DB SETUP ---
conn = sqlite3.connect("opportunities.db", check_same_thread=False)
c = conn.cursor()

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

# --- UI ---
st.set_page_config(page_title="📋 Opportunity Listings", layout="wide")
st.title("📋 Public Opportunity Board")
st.caption("These are publicly listed competitions, internships, and job opportunities.")

entries = load_entries()
if entries:
    st.dataframe(entries, use_container_width=True, hide_index=True)
else:
    st.info("No data yet. Check back later.")
