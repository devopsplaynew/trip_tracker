import streamlit as st
import hashlib
from datetime import datetime, timedelta

# Simple authentication system
CREDENTIALS = {
    "admin": "yelagiri"
}

def check_password():
    """Returns True if the user has entered correct credentials."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in CREDENTIALS:
            if st.session_state["password"] == CREDENTIALS[st.session_state["username"]]:
                st.session_state["authenticated"] = True
                st.session_state["login_time"] = datetime.now()
                del st.session_state["password"]  # Don't store password
            else:
                st.session_state["authenticated"] = False
                st.session_state["login_error"] = "😕 Invalid password"
        else:
            st.session_state["authenticated"] = False
            st.session_state["login_error"] = "😕 Invalid username"

    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["login_error"] = ""

    if not st.session_state["authenticated"]:
        # Login form
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #1E3D59; font-size: 2rem;'>✈️ Trip Expense Tracker</h1>
            <p style='color: #6c757d; font-size: 1rem; margin-bottom: 30px;'>Yelagiri Trip 2024</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Username", key="username", placeholder="Enter username")
            st.text_input("Password", type="password", key="password", placeholder="Enter password")
            
            if st.session_state.get("login_error"):
                st.error(st.session_state["login_error"])
            
            st.button("🔐 Login", on_click=password_entered, use_container_width=True)
        
        return False
    else:
        # Check if session is expired (24 hours)
        if "login_time" in st.session_state:
            if datetime.now() - st.session_state["login_time"] > timedelta(hours=24):
                st.session_state["authenticated"] = False
                st.rerun()
        
        return True

def logout():
    """Logout the user"""
    st.session_state["authenticated"] = False
    if "username" in st.session_state:
        del st.session_state["username"]
    st.rerun()
