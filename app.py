import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import Database
from utils.styles import apply_mobile_styles
from utils.auth import check_password, is_admin, get_current_user, logout
from utils.whatsapp_notifier import WhatsAppNotifier

# Page Configuration
st.set_page_config(
    page_title="Trip Expense Tracker",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply mobile styles
apply_mobile_styles()

# Check authentication
if not check_password():
    st.stop()

# Initialize database and notifier
db = Database()
notifier = WhatsAppNotifier()

# App Header with user info and logout
col_header1, col_header2, col_header3 = st.columns([4, 2, 1])
with col_header1:
    st.markdown("""
    <div class="app-header">
        <h2 style="margin: 0; font-size: 1.3rem;">✈️ Trip Expense Tracker</h2>
    </div>
    """, unsafe_allow_html=True)
with col_header2:
    user_role = "👑 Admin" if is_admin() else "👤 User"
    st.markdown(f"<p style='text-align: center; padding-top: 10px;'>{user_role}: <strong>{get_current_user()}</strong></p>", unsafe_allow_html=True)
with col_header3:
    if st.button("🚪", key="logout_btn", help="Logout", use_container_width=True):
        logout()

# Main Tabs
if is_admin():
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Add", "✅ Approve", "📊 Dashboard", "📜 History"])
else:
    tab1, tab2, tab3 = st.tabs(["📝 Add", "📊 Dashboard", "📜 History"])

# Tab 1: Add Transaction
with tab1:
    with st.form("transaction_form", clear_on_submit=True):
        name = st.text_input("👤 Name", placeholder="Enter name...")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            place = st.text_input("📍 Place/Item", placeholder="e.g., Hotel")
        with col2:
            trans_date = st.date_input("📅 Date", value=datetime.now())
        with col3:
            amount = st.number_input("💰 Amount (₹)", min_value=1, step=10, value=100)
        
        trans_type = st.radio(
            "Type",
            ["💚 Income", "❤️ Expense"],
            horizontal=True
        )
        
        comments = st.text_input("📝 Note (optional)", placeholder="Add note...", max_chars=100)
        
        submitted = st.form_submit_button("✅ Add Transaction", use_container_width=True)
        
        if submitted:
            if not name or not place or amount <= 0:
                st.error("⚠️ Please fill all fields")
            else:
                mapped_type = "Income" if "Income" in trans_type else "Expense"
                trans = db.add_transaction(
                    name, place, amount, mapped_type, comments, 
                    trans_date.strftime("%d-%m-%Y"), 
                    get_current_user()
                )
                
                # Send WhatsApp notification for new entry
                notifier.notify_new_transaction(name, mapped_type, amount, place)
                
                if is_admin():
                    # Auto-approve if admin adds
                    db.approve_transaction(trans["id"], get_current_user())
                    st.success(f"✅ Added & Approved for {name.strip().title()}!")
                else:
                    st.success(f"✅ Added for {name.strip().title()}! Pending admin approval.")
                st.balloons()

# Tab 2: Approve (Admin Only)
if is_admin():
    with tab2:
        st.markdown("### ✅ Pending Approvals")
        
        pending = db.get_pending_transactions()
        
        if not pending:
            st.info("🎉 No pending transactions to approve!")
        else:
            st.markdown(f"<p style='color: #dc3545;'>{len(pending)} transactions pending approval</p>", unsafe_allow_html=True)
            
            for trans in pending:
                trans_type_class = "transaction-income" if trans["type"] == "Income" else "transaction-expense"
                trans_icon = "💚" if trans["type"] == "Income" else "❤️"
                
                col1, col2, col3, col4 = st.columns([3, 1.5, 0.7, 0.7])
                
                with col1:
                    st.markdown(f"""
                    <div class="transaction-item {trans_type_class}">
                        <div>
                            <strong>{trans_icon} {trans['name']}</strong> - {trans['place']}<br>
                            <small style="color: #6c757d;">
                                📅 {trans.get('date', '')} | Added by: {trans.get('added_by', 'Unknown')}<br>
                                💬 {trans.get('comments', 'No comments')}
                            </small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    amount_color = "#11998e" if trans["type"] == "Income" else "#eb3349"
                    st.markdown(f"""
                    <div style="text-align: right; padding: 15px;">
                        <span style="color: {amount_color}; font-weight: bold; font-size: 1.1rem;">
                            ₹{trans['amount']:,.0f}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if st.button("✅", key=f"approve_{trans['id']}", help="Approve"):
                        db.approve_transaction(trans['id'], get_current_user())
                        notifier.notify_transaction_approved(
                            trans['name'], trans['type'], trans['amount'], trans['place']
                        )
                        st.success("Approved!")
                        st.rerun()
                
                with col4:
                    if st.button("❌", key=f"reject_{trans['id']}", help="Reject/Delete"):
                        deleted_trans = db.delete_transaction(trans['id'], get_current_user())
                        if deleted_trans:
                            notifier.notify_transaction_deleted(
                                deleted_trans['name'], deleted_trans['type'], 
                                deleted_trans['amount'], deleted_trans['place'], get_current_user()
                            )
                        st.success("Rejected!")
                        st.rerun()

# Tab 3: Dashboard
dashboard_tab = tab3 if is_admin() else tab2
with dashboard_tab:
    summary = db.get_summary(only_approved=True)
    
    if summary is None:
        st.info("📊 No approved transactions yet. Start adding!")
    else:
        # Compact KPI Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="income-card slide-in">
                <p class="card-title">💰 Total Pool</p>
                <p class="card-amount">₹{summary['total_income']:,.0f}</p>
                <p class="card-subtitle">Income contributed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="expense-card slide-in">
                <p class="card-title">💸 Total Spent</p>
                <p class="card-amount">₹{summary['total_expense']:,.0f}</p>
                <p class="card-subtitle">Out-of-pocket</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            balance = summary['total_income'] - summary['total_expense']
            balance_color = "#38ef7d" if balance >= 0 else "#f45c43"
            st.markdown(f"""
            <div class="compact-card slide-in">
                <p class="card-title">⚖️ Balance</p>
                <p class="card-amount" style="color: {balance_color};">₹{balance:,.0f}</p>
                <p class="card-subtitle">Net balance</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Send Summary via WhatsApp button (Admin only)
        if is_admin():
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("📱 Send Summary via WhatsApp", use_container_width=True):
                    if notifier.send_trip_summary(summary):
                        st.success("✅ Summary sent via WhatsApp!")
                    else:
                        st.warning("WhatsApp not configured. Check settings.")
        
        # Per Person Breakdown
        st.markdown("### 👥 Individual Summary")
        display_df = pd.DataFrame(summary['per_person'])[['Name', 'Total Income', 'Total Expense', 'Net Balance']]
        
        def color_balance(val):
            if '-' in str(val):
                return 'color: #dc3545; font-weight: bold;'
            return 'color: #28a745; font-weight: bold;'
        
        styled_df = display_df.style.applymap(color_balance, subset=['Net Balance'])
        st.dataframe(styled_df, use_container_width=True, height=200, hide_index=True)
        
        # Chart
        st.markdown("### 📊 Overview Chart")
        names = [d['Name'] for d in summary['per_person']]
        incomes = [d['Income_Raw'] for d in summary['per_person']]
        expenses = [d['Expense_Raw'] for d in summary['per_person']]
        
        fig = go.Figure(data=[
            go.Bar(name='Income', x=names, y=incomes, marker_color='#11998e',
                   text=[f"₹{x:,.0f}" for x in incomes], textposition='auto'),
            go.Bar(name='Expense', x=names, y=expenses, marker_color='#eb3349',
                   text=[f"₹{x:,.0f}" for x in expenses], textposition='auto')
        ])
        
        fig.update_layout(
            barmode='group', height=300,
            margin=dict(t=10, b=10, l=10, r=10),
            font=dict(size=11),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

# Tab: History
history_tab = tab4 if is_admin() else tab3
with history_tab:
    transactions = db.get_all_transactions(include_pending=is_admin())
    
    if not transactions:
        st.info("📜 No transactions yet")
    else:
        st.markdown("### 📜 Transaction History")
        
        # Filters
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        with col_filter1:
            filter_type = st.selectbox("Type", ["All", "Income", "Expense"])
        with col_filter2:
            unique_names = list(set(t['name'] for t in transactions))
            filter_name = st.selectbox("Name", ["All"] + sorted(unique_names))
        with col_filter3:
            if is_admin():
                filter_status = st.selectbox("Status", ["All", "Approved", "Pending"])
            else:
                filter_status = "Approved"
        
        # Apply filters
        filtered_transactions = transactions
        if filter_type != "All":
            filtered_transactions = [t for t in filtered_transactions if t['type'] == filter_type]
        if filter_name != "All":
            filtered_transactions = [t for t in filtered_transactions if t['name'] == filter_name]
        if is_admin() and filter_status != "All":
            is_approved = filter_status == "Approved"
            filtered_transactions = [t for t in filtered_transactions if t.get('approved', False) == is_approved]
        
        st.markdown(f"<small>Showing {len(filtered_transactions)} transactions</small>", unsafe_allow_html=True)
        
        # Display transactions
        st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
        
        for trans in filtered_transactions:
            trans_type_class = "transaction-income" if trans["type"] == "Income" else "transaction-expense"
            trans_icon = "💚" if trans["type"] == "Income" else "❤️"
            
            # Approval status indicator
            status_badge = ""
            if is_admin():
                if trans.get("approved", False):
                    status_badge = " ✅"
                else:
                    status_badge = " ⏳"
            
            col1, col2, col3 = st.columns([3, 1, 0.5])
            
            with col1:
                date_display = trans.get('date', trans.get('timestamp', ''))
                if date_display:
                    date_display = f"📅 {date_display}"
                
                st.markdown(f"""
                <div class="transaction-item {trans_type_class}">
                    <div>
                        <strong>{trans_icon} {trans['name']}{status_badge}</strong> - {trans['place']}<br>
                        <small style="color: #6c757d;">
                            {trans.get('comments', '')} {date_display}<br>
                            Added by: {trans.get('added_by', 'Unknown')}
                            {f" | Approved by: {trans.get('approved_by', '')}" if trans.get('approved') else " | ⏳ Pending"}
                        </small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                amount_color = "#11998e" if trans["type"] == "Income" else "#eb3349"
                st.markdown(f"""
                <div style="text-align: right; padding: 10px;">
                    <span style="color: {amount_color}; font-weight: bold; font-size: 1.1rem;">
                        ₹{trans['amount']:,.0f}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if is_admin():
                    if st.button("🗑️", key=f"del_{trans['id']}", help="Delete"):
                        deleted_trans = db.delete_transaction(trans['id'], get_current_user())
                        if deleted_trans:
                            notifier.notify_transaction_deleted(
                                deleted_trans['name'], deleted_trans['type'],
                                deleted_trans['amount'], deleted_trans['place'], get_current_user()
                            )
                        st.success("Deleted!")
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Export and Reset (Admin only)
        if is_admin():
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                df_export = pd.DataFrame(transactions)
                csv = df_export.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"trip_expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col2:
                if st.button("🗑️ Reset All", use_container_width=True):
                    confirm = st.checkbox("Confirm reset?")
                    if confirm:
                        db.clear_all()
                        st.success("All cleared!")
                        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #6c757d; font-size: 0.8rem;'>Trip Expense Tracker | Made with ❤️</p>",
    unsafe_allow_html=True
)
