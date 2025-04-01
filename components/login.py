import streamlit as st
from utils.auth import show_login_ui, show_signup_ui, demo_login

def show_login_page():
    """
    Display the login page.
    """
    st.markdown(
        """
        <div style="text-align: center; animation: fadeIn 1.5s ease-in-out;">
            <h1 style="color: #00E676; text-shadow: 0 0 15px rgba(0, 230, 118, 0.8); margin-bottom: 0.5rem;">
                <span style="display: inline-block; animation: pulse 2s infinite;">💰</span> 
                AI Finance Assistant
            </h1>
            <p style="color: rgba(255,255,255,0.8); font-style: italic; margin-top: 0; margin-bottom: 30px;">
                Your smart money manager
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Create tabs for login and signup
    tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Demo Login"])
    
    with tab1:
        st.markdown("<h3 style='text-align: center;'>Log in to your account</h3>", unsafe_allow_html=True)
        show_login_ui()
    
    with tab2:
        st.markdown("<h3 style='text-align: center;'>Create a new account</h3>", unsafe_allow_html=True)
        show_signup_ui()
        
    with tab3:
        st.markdown("<h3 style='text-align: center;'>Try with demo login</h3>", unsafe_allow_html=True)
        st.markdown(
            """
            <p style="text-align: center; color: rgba(255,255,255,0.7);">
                For testing without Clerk API keys, use the demo login below.
            </p>
            """,
            unsafe_allow_html=True
        )
        demo_login()
    
    # Footer
    st.markdown(
        """
        <div style="position: fixed; bottom: 0; left: 0; right: 0; background-color: rgba(30, 30, 30, 0.7); 
                 padding: 10px; text-align: center; backdrop-filter: blur(5px);">
            <p style="margin: 0; color: rgba(255,255,255,0.6); font-size: 12px;">
                © 2025 AI Finance Assistant. All rights reserved.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )