import streamlit as st
import sqlite3
import pandas as pd

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
conn = sqlite3.connect("opportunities.db", check_same_thread=False)
c = conn.cursor()

# ----------------------------
# HELPER FUNCTION TO LOAD ENTRIES
# ----------------------------
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
# STREAMLIT UI FOR PUBLIC
# ----------------------------
st.set_page_config(page_title="📣 Public Opportunity Board", layout="centered")
st.title("📣 Public Opportunity Board")
st.caption("View competitions, internships, and job listings available.")

entries = load_entries()

if entries:
    st.dataframe(pd.DataFrame(entries), use_container_width=True, hide_index=True)
else:
    st.info("No entries yet. Please check back later.")
