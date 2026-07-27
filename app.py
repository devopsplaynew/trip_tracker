import streamlit as st
import pandas as pd

# 1. Page Configuration (Enterprise Theme & Mobile Responsive)
st.set_page_config(
    page_title="GlobeTrek | Enterprise Expense Suite",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Trip-Themed CSS UI Inject
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e9ecef; box-shadow: 0 4px 6px rgba(0,0,0,0.02); }
        div[data-testid="stForm"] { background-color: #ffffff; border-radius: 12px; padding: 25px; border: 1px solid #e9ecef; box-shadow: 0 4px 12px rgba(0,0,0,0.04); }
        .stButton>button { width: 100%; border-radius: 6px; font-weight: 600; }
        h1, h2, h3 { color: #1e293b; font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# 2. Initialize Session State
if "transactions" not in st.session_state:
    st.session_state.transactions = [
        {"Name": "Alice", "Place/Item": "Grand Plaza Hotel", "Amount": 300.00, "Type": "Income (Pool Contribution)", "Category": "Lodging", "Comments": "Initial pool funding"},
        {"Name": "Bob", "Place/Item": "Grand Plaza Hotel", "Amount": 300.00, "Type": "Income (Pool Contribution)", "Category": "Lodging", "Comments": "Initial pool funding"},
        {"Name": "Alice", "Place/Item": "Airport Shuttle", "Amount": 65.50, "Type": "Expense (Out of Pocket)", "Category": "Transport", "Comments": "Van for group"},
        {"Name": "Bob", "Place/Item": "Seafood Diner", "Amount": 120.00, "Type": "Expense (Out of Pocket)", "Category": "Food", "Comments": "Welcome team dinner"},
        {"Name": "Charlie", "Place/Item": "Museum Passes", "Amount": 45.00, "Type": "Expense (Out of Pocket)", "Category": "Entertainment", "Comments": "Tickets"}
    ]

# 3. Sidebar Header & Configuration Controls
with st.sidebar:
    st.markdown("## ✈️ GlobeTrek Suite")
    st.markdown("*Corporate & Group Expense Management*")
    st.divider()
    
    st.subheader("⚙️ System Control")
    currency = st.selectbox("Preferred Currency", ["USD ($)", "EUR (€)", "GBP (£)", "INR (₹)"])
    curr_sym = currency.split(" ")[1].replace("(", "").replace(")", "")
    
    st.divider()
    st.markdown("### 📥 Portable Data Exchange")
    if st.session_state.transactions:
        df_export = pd.DataFrame(st.session_state.transactions)
        csv = df_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Ledger Report (CSV)",
            data=csv,
            file_name="trip_expense_ledger.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    if st.button("Reset Master Database", type="secondary"):
        st.session_state.transactions = []
        st.rerun()

# 4. Main App Branding Layout
st.title("💼 Enterprise Trip Expense Ledger")
st.caption("Synchronized multi-party balance settlement system for global travel tracking.")
st.divider()

# 5. Core Operational Columns
col_form, col_analytics = st.columns([1, 2], gap="large")

with col_form:
    st.subheader("📝 Record Entry")
    with st.form("enterprise_expense_form", clear_on_submit=True):
        name = st.text_input("Traveller Name", placeholder="Enter full name").strip().title()
        place = st.text_input("Vendor / Place Name", placeholder="e.g., Chevron Gas, Hilton").strip().title()
        amount = st.number_input(f"Transaction Amount ({curr_sym})", min_value=0.01, step=5.00, format="%.2f")
        
        trans_type = st.radio(
            "Transaction Ledger Type",
            options=["Income (Pool Contribution)", "Expense (Out of Pocket)"],
            help="Income feeds the collective trip pot. Expenses are paid out of the traveler's personal funds."
        )
        
        category = st.selectbox(
            "Expense Segment Classification",
            options=["Lodging", "Transport", "Food", "Entertainment", "Utilities", "Other"]
        )
        
        comments = st.text_input("Operational Comments (Optional)", placeholder="Add context...")
        
        submit_button = st.form_submit_button("Commit Transaction to Ledger", type="primary")

    if submit_button:
        if not name or not place:
            st.error("Validation Error: Traveller Name and Vendor/Place fields are required.")
        else:
            new_entry = {
                "Name": name,
                "Place/Item": place,
                "Amount": float(amount),
                "Type": trans_type,
                "Category": category,
                "Comments": comments.strip()
            }
            st.session_state.transactions.append(new_entry)
            st.toast(f"Success: Record logged for {name}!", icon="✅")
            st.rerun()

with col_analytics:
    st.subheader("📊 Analytical Balance & Summaries")
    
    if not st.session_state.transactions:
        st.info("The ledger is currently clear. Enter a transaction in the left pane to initialize processing.")
    else:
        df = pd.DataFrame(st.session_state.transactions)
        
        # High-level KPI calculation
        tot_inc = df[df["Type"] == "Income (Pool Contribution)"]["Amount"].sum()
        tot_exp = df[df["Type"] == "Expense (Out of Pocket)"]["Amount"].sum()
        net_cash = tot_inc - tot_exp
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total Pool Assets (Income)", f"{curr_sym}{tot_inc:,.2f}")
        kpi2.metric("Total Liabilities (Expenses)", f"{curr_sym}{tot_exp:,.2f}")
        kpi3.metric("Net Vault Pool Remainder", f"{curr_sym}{net_cash:,.2f}", delta=f"{net_cash:,.2f}")
        st.divider()
        
        # Individual Breakdown calculations
        st.markdown("### 👥 Per-Person Matrix Breakdown")
        unique_members = df["Name"].unique()
        summary_rows = []
        
        for member in unique_members:
            m_df = df[df["Name"] == member]
            m_inc = m_df[m_df["Type"] == "Income (Pool Contribution)"]["Amount"].sum()
            m_exp = m_df[m_df["Type"] == "Expense (Out of Pocket)"]["Amount"].sum()
            summary_rows.append({
                "Traveller Name": member,
                f"Total Income ({curr_sym})": m_inc,
                f"Total Expense ({curr_sym})": m_exp,
                f"Net Investment ({curr_sym})": m_inc + m_exp
            })
            
        summary_df = pd.DataFrame(summary_rows).set_index("Traveller Name")
        st.dataframe(summary_df, use_container_width=True)
        
        # Peer-To-Peer Settlement Engine (Enterprise feature)
        st.markdown("### ⚖️ Auto-Settlement Engine (Who owes whom)")
        
        # Calculation formula: Total expenses split equally vs what they already paid
        total_trip_cost = tot_exp
        num_people = len(unique_members)
        
        if num_people > 1 and total_trip_cost > 0:
            share_per_person = total_trip_cost / num_people
            st.caption(f"Target equal share per individual for this trip: **{curr_sym}{share_per_person:,.2f}**")
            
            balances = {}
            for member in unique_members:
                m_df = df[df["Name"] == member]
                # What they actually paid out of pocket
                paid = m_df[m_df["Type"] == "Expense (Out of Pocket)"]["Amount"].sum()
                balances[member] = paid - share_per_person
                
            debtors = []
            creditors = []
            
            for person, bal in balances.items():
                if bal < -0.01:
                    debtors.append({"name": person, "amount": abs(bal)})
                elif bal > 0.01:
                    creditors.append({"name": person, "amount": bal})
                    
            settlement_actions = []
            d_idx, c_idx = 0, 0
            
            while d_idx < len(debtors) and c_idx < len(creditors):
                deb = debtors[d_idx]
                cred = creditors[c_idx]
                
                settle_amt = min(deb["amount"], cred["amount"])
                settlement_actions.append(f"👉 **{deb['name']}** pays **{curr_sym}{settle_amt:,.2f}** to **{cred['name']}**")
                
                deb["amount"] -= settle_amt
                cred["amount"] -= settle_amt
                
                if deb["amount"] <= 0.01: d_idx += 1
                if cred["amount"] <= 0.01: c_idx += 1
                
            if settlement_actions:
                for action in settlement_actions:
                    st.info(action)
            else:
                st.success("🎉 All balances are perfectly settled evenly among members!")
        else:
            st.warning("Add expense logs for multiple travellers to compute cross-party balancing actions.")
            
        # Complete Logs History Table
        st.divider()
        st.markdown("### 📜 Real-Time Master Audit Ledger")
        st.dataframe(df, use_container_width=True)
