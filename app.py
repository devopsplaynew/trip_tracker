import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import Database
from utils.styles import apply_custom_styles

# Page Configuration
st.set_page_config(
    page_title="Trip Expense Tracker",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
apply_custom_styles()

# Initialize database
db = Database()

# App Header
st.markdown("""
<div class="animate-fade-in">
    <h1 style="text-align: center; color: #1E3D59; margin-bottom: 10px;">✈️ Trip Expense Tracker</h1>
    <p style="text-align: center; color: #6c757d; font-size: 1.2rem; margin-bottom: 30px;">
        Track group contributions and expenses in real-time
    </p>
</div>
""", unsafe_allow_html=True)

# Tabs for better organization
tab1, tab2, tab3 = st.tabs(["📝 Add Transaction", "📊 Dashboard", "📜 History"])

with tab1:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Add New Transaction")
        
        with st.form("transaction_form", clear_on_submit=True):
            name = st.text_input("👤 Your Name", placeholder="Enter your name...")
            
            col_form1, col_form2 = st.columns(2)
            with col_form1:
                place = st.text_input("📍 Place/Item", placeholder="e.g., Hotel, Restaurant")
            with col_form2:
                amount = st.number_input("💰 Amount ($)", min_value=0.01, step=1.0, format="%.2f")
            
            trans_type = st.radio(
                "Transaction Type",
                ["💚 Income (Money Added to Pool)", "❤️ Expense (Money Spent)"],
                horizontal=True
            )
            
            comments = st.text_area("📝 Comments (Optional)", placeholder="Add any notes...", max_chars=200)
            
            submitted = st.form_submit_button("✅ Add Transaction", use_container_width=True)
            
            if submitted:
                if not name or not place or amount <= 0:
                    st.error("⚠️ Please fill in all required fields with valid values.")
                else:
                    mapped_type = "Income" if "Income" in trans_type else "Expense"
                    db.add_transaction(name, place, amount, mapped_type, comments)
                    st.success(f"✅ Transaction added successfully for {name.strip().title()}!")
                    st.balloons()

with tab2:
    summary = db.get_summary()
    
    if summary is None:
        st.info("📊 No transactions yet. Start by adding some transactions in the 'Add Transaction' tab!")
    else:
        # Top KPI Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="income-card">
                <h3 style="margin: 0;">💰 Total Pool</h3>
                <h2 style="margin: 10px 0;">${summary['total_income']:,.2f}</h2>
                <p style="margin: 0; font-size: 0.9rem;">Total income contributed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="expense-card">
                <h3 style="margin: 0;">💸 Total Spent</h3>
                <h2 style="margin: 10px 0;">${summary['total_expense']:,.2f}</h2>
                <p style="margin: 0; font-size: 0.9rem;">Total out-of-pocket expenses</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            balance = summary['total_income'] - summary['total_expense']
            balance_color = "green" if balance >= 0 else "red"
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 15px; padding: 20px; color: white; 
                        box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                <h3 style="margin: 0;">⚖️ Net Balance</h3>
                <h2 style="margin: 10px 0; color: {balance_color};">${balance:,.2f}</h2>
                <p style="margin: 0; font-size: 0.9rem;">Income minus expenses</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Section
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("### 📊 Income vs Expense Distribution")
            # Create pie chart
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Income', 'Expense'],
                values=[summary['total_income'], summary['total_expense']],
                hole=.4,
                marker_colors=['#11998e', '#eb3349']
            )])
            fig_pie.update_layout(
                showlegend=True,
                height=400,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_chart2:
            st.markdown("### 👥 Per Person Breakdown")
            # Create bar chart
            per_person_data = pd.DataFrame(summary['per_person'])
            
            fig_bar = go.Figure(data=[
                go.Bar(name='Income', x=per_person_data['Name'], 
                      y=per_person_data['Income_Raw'], 
                      marker_color='#11998e'),
                go.Bar(name='Expense', x=per_person_data['Name'], 
                      y=per_person_data['Expense_Raw'], 
                      marker_color='#eb3349')
            ])
            fig_bar.update_layout(
                barmode='group',
                height=400,
                margin=dict(t=0, b=0, l=0, r=0),
                xaxis_title="Person",
                yaxis_title="Amount ($)"
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Detailed Table
        st.markdown("### 📋 Individual Breakdown")
        display_df = pd.DataFrame(summary['per_person'])[['Name', 'Total Income', 'Total Expense', 'Net Balance']]
        st.dataframe(
            display_df.set_index('Name'),
            use_container_width=True,
            height=200
        )

with tab3:
    summary = db.get_summary()
    
    if summary is None:
        st.info("📜 No transaction history yet.")
    else:
        st.markdown("### 📜 Complete Transaction History")
        
        # Filters
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            filter_name = st.selectbox(
                "Filter by Name",
                ["All"] + list(summary['all_transactions']["name"].unique())
            )
        with col_filter2:
            filter_type = st.selectbox(
                "Filter by Type",
                ["All", "Income", "Expense"]
            )
        
        # Apply filters
        filtered_df = summary['all_transactions']
        if filter_name != "All":
            filtered_df = filtered_df[filtered_df["name"] == filter_name]
        if filter_type != "All":
            filtered_df = filtered_df[filtered_df["type"] == filter_type]
        
        # Display filtered data
        display_cols = ['name', 'place', 'amount', 'type', 'comments', 'timestamp']
        st.dataframe(
            filtered_df[display_cols].rename(columns={
                'name': 'Name',
                'place': 'Place',
                'amount': 'Amount ($)',
                'type': 'Type',
                'comments': 'Comments',
                'timestamp': 'Date/Time'
            }),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Transaction History",
            data=csv,
            file_name=f"trip_expenses_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

# Sidebar
with st.sidebar:
    st.markdown("### 🎯 Quick Stats")
    
    transaction_count = db.get_transaction_count()
    st.metric("Total Transactions", transaction_count)
    
    if transaction_count > 0:
        summary = db.get_summary()
        st.metric("Participants", len(summary['per_person']))
        st.metric("Average per Transaction", f"${(summary['total_income'] + summary['total_expense'])/transaction_count:,.2f}")
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.info("""
    This app helps you track group expenses during trips.
    
    **Income:** Money added to the common pool
    **Expense:** Money spent from personal pocket
    
    All data is stored permanently on the server.
    """)
    
    st.markdown("---")
    
    # Reset button
    if st.button("🗑️ Reset All Data", use_container_width=True):
        if st.warning("Are you sure? This cannot be undone!"):
            if st.button("Yes, delete everything"):
                db.clear_all()
                st.success("All data has been cleared!")
                st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #6c757d;'>Trip Expense Tracker © 2024 | Made with ❤️ using Streamlit</p>",
    unsafe_allow_html=True
)
