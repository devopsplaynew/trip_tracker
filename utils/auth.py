import streamlit as st
from datetime import datetime, timedelta

# Authentication system with roles
CREDENTIALS = {
    "admin": {
        "password": "great",
        "role": "admin",
        "name": "Administrator"
    },
    "user1": {
        "password": "trip2024",
        "role": "user",
        "name": "Team Member"
    }
}

def check_password():
    """Returns True if the user has entered correct credentials."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        username = st.session_state.get("username", "").lower()
        password = st.session_state.get("password", "")
        
        if username in CREDENTIALS:
            if password == CREDENTIALS[username]["password"]:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["user_role"] = CREDENTIALS[username]["role"]
                st.session_state["user_name"] = CREDENTIALS[username]["name"]
                st.session_state["login_time"] = datetime.now()
                if "password" in st.session_state:
                    del st.session_state["password"]
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
        st.session_state["user_role"] = None

    if not st.session_state["authenticated"]:
        # Login form
        st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #1E3D59; font-size: 2rem;'>✈️ Trip Expense Tracker</h1>
            <p style='color: #6c757d; font-size: 1rem; margin-bottom: 30px;'>Track your group expenses easily</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Username", key="username", placeholder="Enter username")
            st.text_input("Password", type="password", key="password", placeholder="Enter password")
            
            if st.session_state.get("login_error"):
                st.error(st.session_state["login_error"])
            
            st.button("🔐 Login", on_click=password_entered, use_container_width=True)
            
            st.markdown("""
            <div style='background: #f8f9fa; padding: 10px; border-radius: 8px; margin-top: 10px;'>
                <small style='color: #6c757d;'>
                    <strong>Demo Credentials:</strong><br>
                    Admin: admin / great<br>
                    User: user1 / trip2024
                </small>
            </div>
            """, unsafe_allow_html=True)
        
        return False
    else:
        # Check if session is expired (24 hours)
        if "login_time" in st.session_state:
            if datetime.now() - st.session_state["login_time"] > timedelta(hours=24):
                st.session_state["authenticated"] = False
                st.rerun()
        
        return True

def is_admin():
    """Check if current user is admin"""
    return st.session_state.get("user_role") == "admin"

def get_current_user():
    """Get current username"""
    return st.session_state.get("username", "Unknown")

def logout():
    """Logout the user"""
    st.session_state["authenticated"] = False
    st.session_state["user_role"] = None
    if "username" in st.session_state:
        del st.session_state["username"]
    st.rerun()
