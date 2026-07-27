import streamlit as st
import pandas as pd
import os
import json

# Set Page Title
st.set_page_config(page_title="Trip Expense Ledger", page_icon="💰", layout="wide")

# Persistent File Configuration on Linux Server
DB_FILE = "trip_database.json"

def load_database():
    """Loads records directly from the permanent JSON file."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_database(data):
    """Saves records permanently to the JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Initialize in-memory session from permanent storage file
if "transactions" not in st.session_state:
    st.session_state.transactions = load_database()

st.title("💰 Trip Ledger & Expense Tracker (INR ₹)")
st.caption("Shared live ledger for our team. Accessible by everyone. Permanent storage enabled.")
st.divider()

# Layout Configuration: Input Form (Left), Live Ledger & Metrics (Right)
col_input, col_view = st.columns([1, 2], gap="large")

with col_input:
    st.subheader("📝 Log New Transaction")
    with st.form("entry_form", clear_on_submit=True):
        name = st.text_input("Person Name", placeholder="e.g., Rajesh").strip().title()
        type_of_trans = st.selectbox("Transaction Action", ["Gave / Contributed to Pool", "Spent Out of Pocket"])
        amount = st.number_input("Amount (₹)", min_value=1.0, step=50.0, format="%.2f")
        place = st.text_input("Place Name / Item", placeholder="e.g., Gas Station, Dhabha").strip().title()
        comments = st.text_area("Comments", placeholder="Add notes here...").strip()
        
        submit = st.form_submit_button("Add to Shared Ledger")

    if submit:
        if not name or not place or amount <= 0:
            st.error("Please enter valid details for Person, Place, and Amount.")
        else:
            # Map type to strict simple categories
            mapped_type = "Gave (Pool)" if "Gave" in type_of_trans else "Spent (Pocket)"
            
            # Form record structure
            new_record = {
                "Person": name,
                "Action": mapped_type,
                "Amount (₹)": float(amount),
                "Place": place,
                "Comments": comments
            }
            
            # Commit to memory and disk storage instantly
            st.session_state.transactions.append(new_record)
            save_database(st.session_state.transactions)
            st.success(f"Added successfully to permanent records!")
            st.rerun()

    # Administrative Action: Direct Data Removal
    if st.session_state.transactions:
        st.divider()
        st.subheader("🗑️ Delete a Row")
        row_to_delete = st.number_input(
            "Enter Row Index # to delete", 
            min_value=0, 
            max_value=len(st.session_state.transactions)-1, 
            step=1
        )
        if st.button("Delete Selected Row From Database", type="secondary"):
            deleted_item = st.session_state.transactions.pop(row_to_delete)
            save_database(st.session_state.transactions)
            st.toast(f"Removed item from {deleted_item['Person']} successfully!", icon="🗑️")
            st.rerun()

with col_view:
    st.subheader("📊 Live Ledger Summary")
    
    if not st.session_state.transactions:
        st.info("No logs present. Use the panel on the left to start tracking.")
    else:
        # Convert to Pandas dataframe
        df = pd.DataFrame(st.session_state.transactions)
        
        # Calculate Per-Person Matrix
        summary_rows = []
        unique_people = df["Person"].unique()
        
        for person in unique_people:
            p_df = df[df["Person"] == person]
            gave = p_df[p_df["Action"] == "Gave (Pool)"]["Amount (₹)"].sum()
            spent = p_df[p_df["Action"] == "Spent (Pocket)"]["Amount (₹)"].sum()
            summary_rows.append({
                "Person": person,
                "Total Gave (₹)": gave,
                "Total Spent (₹)": spent
            })
            
        summary_df = pd.DataFrame(summary_rows)
        
        # Display Totals Dashboard Metrics
        total_pool_gave = df[df["Action"] == "Gave (Pool)"]["Amount (₹)"].sum()
        total_out_spent = df[df["Action"] == "Spent (Pocket)"]["Amount (₹)"].sum()
        
        m1, m2 = st.columns(2)
        m1.metric("Total Pool Cash Given", f"₹{total_pool_gave:,.2f}")
        m2.metric("Total Pocket Expenses Spent", f"₹{total_out_spent:,.2f}")
        
        # Display Individual Totals Matrix
        st.markdown("### 👥 Personal Breakdown Matrix")
        st.dataframe(summary_df.set_index("Person"), use_container_width=True)
        
        # Display Simple Bar Chart Representation
        st.markdown("### 📈 Visual Balance Comparison")
        chart_data = summary_df.set_index("Person")
        st.bar_chart(chart_data)
        
        # Master Log Table
        st.markdown("### 📜 Shared Audit Table Ledger")
        st.dataframe(df, use_container_width=True)
