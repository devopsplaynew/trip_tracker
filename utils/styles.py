import streamlit as st

def apply_mobile_styles():
    st.markdown("""
    <style>
    /* Mobile-first responsive design */
    @media (max-width: 768px) {
        .stApp {
            padding: 0 !important;
        }
        
        .main > div {
            padding: 0.5rem !important;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        h2 {
            font-size: 1.2rem !important;
        }
        
        h3 {
            font-size: 1rem !important;
        }
    }
    
    /* Compact cards */
    .compact-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 12px 15px;
        color: white;
        margin-bottom: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .income-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 10px;
        padding: 12px 15px;
        color: white;
        margin-bottom: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .expense-card {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        border-radius: 10px;
        padding: 12px 15px;
        color: white;
        margin-bottom: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .card-title {
        font-size: 0.85rem;
        margin: 0;
        opacity: 0.9;
    }
    
    .card-amount {
        font-size: 1.3rem;
        margin: 3px 0;
        font-weight: bold;
    }
    
    .card-subtitle {
        font-size: 0.7rem;
        margin: 0;
        opacity: 0.8;
    }
    
    /* Compact form elements */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 8px 12px;
        font-size: 0.9rem;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Delete button */
    .delete-btn {
        background-color: #dc3545;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 4px 8px;
        font-size: 0.75rem;
        cursor: pointer;
    }
    
    /* Tables */
    .dataframe {
        font-size: 0.85rem !important;
    }
    
    .dataframe th {
        padding: 6px 8px !important;
        background-color: #f8f9fa !important;
    }
    
    .dataframe td {
        padding: 5px 8px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 0.85rem;
    }
    
    /* Headers */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: white;
        text-align: center;
    }
    
    /* Transaction list items */
    .transaction-item {
        background: white;
        border-left: 4px solid #667eea;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .transaction-income {
        border-left-color: #11998e;
    }
    
    .transaction-expense {
        border-left-color: #eb3349;
    }
    
    /* Scrollable container */
    .scroll-container {
        max-height: 400px;
        overflow-y: auto;
        padding-right: 5px;
    }
    
    /* Logout button */
    .logout-btn {
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 1000;
    }
    
    /* Animations */
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    .slide-in {
        animation: slideIn 0.3s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
