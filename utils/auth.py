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
    
    cookie_manager = stx.CookieManager()
    clerk_token = cookie_manager.get(cookie="__clerk_session_jwt")
    
    # If we have a token and are not authenticated, set authenticated to True
    if clerk_token and not st.session_state.authenticated:
        st.session_state.authenticated = True
        # In a real implementation, you would decode and verify the JWT here
        # and retrieve real user data
        
        # For demonstration purposes, we'll set default values
        if not st.session_state.user_id:
            st.session_state.user_id = "demo_user_id"
        if not st.session_state.user_name:
            st.session_state.user_name = "Demo User"
        if not st.session_state.user_email:
            st.session_state.user_email = "demo@example.com"
    
    # If we don't have a token but are authenticated, set authenticated to False
    elif not clerk_token and st.session_state.authenticated:
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.user_email = None
    
    return st.session_state.authenticated

def show_login_ui():
    """
    Display the Clerk login UI.
    """
    st.markdown(
        f"""
        <div id="clerk-sign-in" style="width: 100%; height: 700px; animation: fadeIn 1s ease-in-out;"></div>
        <script src="https://js.clerk.io/v1/clerk.js"></script>
        <script>
            const clerkPublishableKey = "{CLERK_PUBLISHABLE_KEY or 'missing_clerk_key'}";
            
            if (!clerkPublishableKey || clerkPublishableKey === 'missing_clerk_key') {{
                document.getElementById('clerk-sign-in').innerHTML = `
                    <div style="border: 2px solid #ff4d4d; padding: 20px; border-radius: 10px; 
                         background-color: rgba(255, 77, 77, 0.1); margin-top: 20px; text-align: center;">
                        <h3 style="color: #ff4d4d;">Clerk API Key Required</h3>
                        <p>To enable authentication, please set up your Clerk API keys in the environment variables.</p>
                    </div>
                `;
            }} else {{
                const clerk = window.Clerk(clerkPublishableKey);
                
                clerk.load({{
                    // Set the sign-in options
                    signIn: {{
                        routing: "path",
                        path: "/sign-in",
                        mount: document.getElementById("clerk-sign-in"),
                        appearance: {{
                            variables: {{
                                colorPrimary: "#00E676",
                                colorBackground: "#121212",
                                colorText: "#FFFFFF",
                                colorInputBackground: "#1E1E1E",
                                colorInputText: "#FFFFFF",
                                fontFamily: "Arial, sans-serif",
                            }},
                            layout: {{
                                socialButtonsVariant: "iconAndText",
                                socialButtonsPlacement: "bottom"
                            }}
                        }}
                    }}
                }});
            }}
        </script>
        """,
        unsafe_allow_html=True,
    )

def show_signup_ui():
    """
    Display the Clerk signup UI.
    """
    st.markdown(
        f"""
        <div id="clerk-sign-up" style="width: 100%; height: 700px; animation: fadeIn 1s ease-in-out;"></div>
        <script src="https://js.clerk.io/v1/clerk.js"></script>
        <script>
            const clerkPublishableKey = "{CLERK_PUBLISHABLE_KEY or 'missing_clerk_key'}";
            
            if (!clerkPublishableKey || clerkPublishableKey === 'missing_clerk_key') {{
                document.getElementById('clerk-sign-up').innerHTML = `
                    <div style="border: 2px solid #ff4d4d; padding: 20px; border-radius: 10px; 
                         background-color: rgba(255, 77, 77, 0.1); margin-top: 20px; text-align: center;">
                        <h3 style="color: #ff4d4d;">Clerk API Key Required</h3>
                        <p>To enable authentication, please set up your Clerk API keys in the environment variables.</p>
                    </div>
                `;
            }} else {{
                const clerk = window.Clerk(clerkPublishableKey);
                
                clerk.load({{
                    // Set the sign-up options
                    signUp: {{
                        routing: "path",
                        path: "/sign-up",
                        mount: document.getElementById("clerk-sign-up"),
                        appearance: {{
                            variables: {{
                                colorPrimary: "#00E676",
                                colorBackground: "#121212",
                                colorText: "#FFFFFF",
                                colorInputBackground: "#1E1E1E",
                                colorInputText: "#FFFFFF",
                                fontFamily: "Arial, sans-serif",
                            }},
                            layout: {{
                                socialButtonsVariant: "iconAndText",
                                socialButtonsPlacement: "bottom"
                            }}
                        }}
                    }}
                }});
            }}
        </script>
        """,
        unsafe_allow_html=True,
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
    A simplified demo login function for testing without Clerk setup.
    """
    email = st.text_input("Email", key="demo_email")
    password = st.text_input("Password", type="password", key="demo_password")
    
    if st.button("Login", key="demo_login_button"):
        # In a real app, you would verify credentials against a database
        # This is just for demonstration purposes
        st.session_state.authenticated = True
        st.session_state.user_id = "demo_user_id"
        st.session_state.user_name = email.split('@')[0].title()
        st.session_state.user_email = email
        st.rerun()