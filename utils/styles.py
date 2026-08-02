import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Headers */
    h1 {
        color: #1E3D59;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #17A2B8;
        font-size: 1.8rem;
        font-weight: 600;
        margin-top: 2rem;
    }
    
    /* Cards */
    .custom-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .income-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .expense-card {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        border-radius: 15px;
        padding: 20px;
        color: white;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 10px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Metrics */
    .metric-container {
        background: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        border-radius: 10px;
    }
    
    /* Success messages */
    .success-message {
        padding: 15px;
        border-radius: 10px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)
