import os
import streamlit as st
import extra_streamlit_components as stx
from datetime import datetime, timedelta

# Clerk keys - these would be set up in your environment variables
# when deployed or in .env file locally
CLERK_PUBLISHABLE_KEY = os.environ.get("CLERK_PUBLISHABLE_KEY")
CLERK_SECRET_KEY = os.environ.get("CLERK_SECRET_KEY")

def initialize_auth():
    """
    Initialize the authentication system.
    """
    # Initialize session state variables
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None

def clerk_auth():
    """
    Handle Clerk authentication using a cookie manager.
    This is a simplified implementation without actual verification.
    In a real app, you would verify these tokens with Clerk's API.
    """
    initialize_auth()
    
    # Check for demo login first (session state already set)
    if st.session_state.authenticated and st.session_state.user_id == "demo_user_id":
        return True
    
    # Try Clerk authentication if API keys are available
    if CLERK_PUBLISHABLE_KEY and CLERK_SECRET_KEY:
        cookie_manager = stx.CookieManager()
        clerk_token = cookie_manager.get(cookie="__clerk_session_jwt")
        
        # If we have a token and are not authenticated, set authenticated to True
        if clerk_token and not st.session_state.authenticated:
            st.session_state.authenticated = True
            # In a real implementation, you would decode and verify the JWT here
            # and retrieve real user data
            
            # For demonstration purposes, we'll set default values
            if not st.session_state.user_id:
                st.session_state.user_id = "clerk_user_id"
            if not st.session_state.user_name:
                st.session_state.user_name = "Clerk User"
            if not st.session_state.user_email:
                st.session_state.user_email = "clerk_user@example.com"
        
        # If we don't have a token but are authenticated, set authenticated to False
        elif not clerk_token and st.session_state.authenticated and st.session_state.user_id != "demo_user_id":
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_name = None
            st.session_state.user_email = None
    
    return st.session_state.authenticated

def show_login_ui():
    """
    Display a simplified login UI since Clerk integration is not working.
    """
    col1, col2 = st.columns([1, 3])
    
    with col2:
        st.markdown(
            """
            <div style="border: 2px solid #00E676; padding: 20px; border-radius: 10px; 
                 background-color: rgba(0, 230, 118, 0.1); margin-top: 20px; text-align: center;">
                <h3 style="color: #00E676;">Login Form</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Simple email input
        email = st.text_input("Email Address", key="login_email", 
                             placeholder="your.email@example.com")
        
        # Password input
        password = st.text_input("Password", type="password", key="login_password")
        
        # Login button with styling
        if st.button("Login", key="login_button", use_container_width=True, type="primary"):
            # Simple validation
            if email and password:
                st.session_state.authenticated = True
                st.session_state.user_id = "user_" + email.split('@')[0]
                st.session_state.user_name = email.split('@')[0].title()
                st.session_state.user_email = email
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Please enter both email and password")
            
        st.markdown(
            """
            <p style="text-align: center; margin-top: 15px;">
                <a href="#" style="color: #00E676; text-decoration: none;">Forgot password?</a>
            </p>
            """, 
            unsafe_allow_html=True
        )

def show_signup_ui():
    """
    Display a simplified signup UI since Clerk integration is not working.
    """
    col1, col2 = st.columns([1, 3])
    
    with col2:
        st.markdown(
            """
            <div style="border: 2px solid #00E676; padding: 20px; border-radius: 10px; 
                 background-color: rgba(0, 230, 118, 0.1); margin-top: 20px; text-align: center;">
                <h3 style="color: #00E676;">Create an Account</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Name input
        full_name = st.text_input("Full Name", key="signup_name", 
                               placeholder="John Doe")
        
        # Email input
        email = st.text_input("Email Address", key="signup_email", 
                             placeholder="your.email@example.com")
        
        # Password inputs
        password = st.text_input("Create Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        
        # Terms and conditions checkbox
        agree_terms = st.checkbox("I agree to the Terms and Conditions", key="signup_terms")
        
        # Signup button with styling
        if st.button("Create Account", key="signup_button", use_container_width=True, type="primary"):
            # Simple validation
            if not full_name or not email or not password or not confirm_password:
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif not agree_terms:
                st.warning("You must agree to the Terms and Conditions")
            else:
                st.session_state.authenticated = True
                st.session_state.user_id = "user_" + email.split('@')[0]
                st.session_state.user_name = full_name
                st.session_state.user_email = email
                st.success("Account created successfully!")
                st.rerun()
                
        st.markdown(
            """
            <p style="text-align: center; margin-top: 15px; color: #AAAAAA;">
                By signing up, you agree to our Terms of Service and Privacy Policy.
            </p>
            """, 
            unsafe_allow_html=True
        )

def show_user_profile():
    """
    Display user profile information.
    """
    st.markdown(
        f"""
        <div style="padding: 20px; border-radius: 10px; 
                  background-color: rgba(0, 230, 118, 0.1); 
                  margin-top: 20px; animation: fadeIn 1s ease-in-out;">
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <div style="width: 50px; height: 50px; border-radius: 50%; 
                          background-color: #00E676; display: flex; 
                          justify-content: center; align-items: center; 
                          font-size: 20px; margin-right: 15px; 
                          color: #121212; font-weight: bold;">
                    {st.session_state.user_name[0].upper() if st.session_state.user_name else '?'}
                </div>
                <div>
                    <h3 style="margin: 0; color: #00E676;">{st.session_state.user_name}</h3>
                    <p style="margin: 0; color: #AAAAAA;">{st.session_state.user_email}</p>
                </div>
            </div>
            <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
            <p style="color: #FFFFFF;">User ID: {st.session_state.user_id}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def logout_button():
    """
    Display a logout button that clears the session when clicked.
    """
    if st.button("Log Out", key="logout_button", 
                 help="Click to log out of your account",
                 use_container_width=True,
                 type="primary"):
        # Clear all session state
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.user_email = None
        
        # Clear Clerk token from cookies
        cookie_manager = stx.CookieManager()
        cookie_manager.delete("__clerk_session_jwt")
        
        st.rerun()

def demo_login():
    """
    A simplified demo login function for testing purposes.
    """
    col1, col2 = st.columns([1, 3])
    
    with col2:
        st.markdown(
            """
            <div style="border: 2px solid #FFD700; padding: 20px; border-radius: 10px; 
                 background-color: rgba(255, 215, 0, 0.1); margin-top: 20px; text-align: center;">
                <h3 style="color: #FFD700;">Demo Login</h3>
                <p style="color: #AAAAAA;">No real authentication - just for demonstration</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Email input with default value
        email = st.text_input("Email", key="demo_email", value="demo@example.com")
        
        # Password input with default value
        password = st.text_input("Password", type="password", key="demo_password", value="demo123")
        
        # Remember me checkbox
        remember_me = st.checkbox("Remember me", key="demo_remember", value=True)
        
        # Login button with styling
        if st.button("Enter Demo Mode", key="demo_login_button", use_container_width=True, 
                   type="primary", help="Log in with demo credentials"):
            # For demo purposes, we'll always log in successfully
            st.session_state.authenticated = True
            st.session_state.user_id = "demo_user_id"
            st.session_state.user_name = "Demo User"
            st.session_state.user_email = email
            st.success("Demo login successful!")
            st.rerun()
            
        st.markdown(
            """
            <p style="text-align: center; margin-top: 15px; color: #AAAAAA;">
                This demo mode uses a pre-populated database with sample financial data.
            </p>
            """, 
            unsafe_allow_html=True
        )