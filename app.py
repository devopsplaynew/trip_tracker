import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Trip Expense Tracker", page_icon="✈️", layout="wide")

# Initialize session state to store transactions if it doesn't exist
if "transactions" not in st.session_state:
    st.session_state.transactions = []

st.title("✈️ Trip Expense Tracker")
st.write("Track group contributions (Income) and out-of-pocket costs (Expenses).")

# Layout: Two columns (Left for Input form, Right for Summary & History)
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📝 Add Transaction")
    with st.form("expense_form", clear_on_submit=True):
        name = st.text_input("Name", placeholder="e.g., Alice")
        place = st.text_input("Place / Item", placeholder="e.g., Gas Station, Hotel")
        amount = st.number_input("Amount ($)", min_value=0.0, step=1.0, format="%.2f")
        
        # Select transaction type
        trans_type = st.selectbox(
            "Transaction Type", 
            options=["Income (Contributed to Pool)", "Expense (Spent Out of Pocket)"]
        )
        
        comments = st.text_area("Comments", placeholder="Optional details...", max_chars=150)
        submit_button = st.form_submit_with_button("Log Transaction")

    if submit_button:
        if name.strip() == "" or place.strip() == "" or amount <= 0:
            st.error("Please fill in Name, Place, and a valid Amount.")
        else:
            # Map friendly selection back to core logic types
            mapped_type = "Income" if "Income" in trans_type else "Expense"
            
            # Save transaction
            new_trans = {
                "Name": name.strip().title(),
                "Place": place.strip().title(),
                "Amount": amount,
                "Type": mapped_type,
                "Comments": comments.strip()
            }
            st.session_state.transactions.append(new_trans)
            st.success(f"Successfully logged {mapped_type} for {name.strip().title()}!")

with col2:
    st.header("📊 Trip Summaries")
    
    if not st.session_state.transactions:
        st.info("No transactions logged yet. Use the form on the left to start.")
    else:
        # Convert list of dicts to a pandas DataFrame for processing
        df = pd.DataFrame(st.session_state.transactions)
        
        # Calculate Per-Person Summaries
        summary_data = []
        unique_names = df["Name"].unique()
        
        for p_name in unique_names:
            p_df = df[df["Name"] == p_name]
            total_income = p_df[p_df["Type"] == "Income"]["Amount"].sum()
            total_expense = p_df[p_df["Type"] == "Expense"]["Amount"].sum()
            summary_data.append({
                "Name": p_name,
                "Total Income": total_income,
                "Total Expense": total_expense
            })
            
        summary_df = pd.DataFrame(summary_data)
        
        # Metric KPI cards for whole trip totals
        total_trip_income = df[df["Type"] == "Income"]["Amount"].sum()
        total_trip_expense = df[df["Type"] == "Expense"]["Amount"].sum()
        
        kpi1, kpi2 = st.columns(2)
        kpi1.metric("Total Trip Pool (Income)", f"${total_trip_income:,.2f}")
        kpi2.metric("Total Money Spent (Expense)", f"${total_trip_expense:,.2f}")
        
        # Display the summarized per-person table
        st.subheader("Individual Breakdown")
        st.dataframe(summary_df.set_index("Name"), use_container_width=True)
        
        # Display raw history logs
        st.subheader("📜 Transaction Log History")
        st.dataframe(df, use_container_width=True)
        
        # Clear data button
        if st.button("Reset All Data"):
            st.session_state.transactions = []
            st.rerun()