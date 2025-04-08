import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json

# Import components
from components.dashboard import show_dashboard
from components.expenses import show_expenses
from components.budget import show_budget
from components.insights import show_insights
from components.goals import show_goals
from components.login import show_login_page

# Import database utilities
from utils.database import (
    init_db, get_all_expenses, get_all_budgets, 
    get_all_goals, get_insights, export_data, import_data
)

# Import authentication utilities
from utils.auth import clerk_auth, initialize_auth, show_user_profile, logout_button

# Import UI utilities
from utils.ui_utils import (
    load_css, add_animation_css, add_logo, animated_text, 
    animated_metric, animated_card, animated_divider, 
    animated_progress_bar, page_header, animated_illustration,
    notification, display_dashboard_widgets, animated_button,
    display_icon, get_icon, get_illustration, display_footer,
    smooth_scroll
)

from static.icons import (
    dashboard_icon, expenses_icon, budget_icon, goals_icon, 
    insights_icon, money_icon, profile_icon, logout_icon
)

# App configuration
st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS and animations
try:
    load_css()  # Try to load the full CSS file
except:
    add_animation_css()  # Fall back to basic animations

# Initialize database
init_db()

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state.expenses = get_all_expenses()
    
if "budgets" not in st.session_state:
    st.session_state.budgets = get_all_budgets()
    
if "goals" not in st.session_state:
    st.session_state.goals = get_all_goals()
    
if "financial_insights" not in st.session_state:
    st.session_state.financial_insights = get_insights()
    
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Add smooth scrolling
smooth_scroll()

# Navigation
pages = {
    "Dashboard": show_dashboard,
    "Expenses": show_expenses,
    "Budget": show_budget,
    "Insights": show_insights,
    "Goals": show_goals
}

# Create a more dynamic sidebar
with st.sidebar:
    # App logo and title with animation
    st.markdown(f"""
    <div style="animation: fadeIn 1.5s ease-in-out; text-align: center; margin-bottom: 20px;">
        <h1 style="color: #00E676; text-shadow: 0 0 15px rgba(0, 230, 118, 0.8); margin-bottom: 0.5rem;">
            <span style="display: inline-block; animation: pulse 2s infinite;">💰</span> 
            Finance AI
        </h1>
        <p style="color: rgba(255,255,255,0.8); font-style: italic; margin-top: 0;">
            Your intelligent financial assistant
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation with icons
    st.markdown("""
    <div style="animation: fadeIn 0.8s ease-in-out;">
        <h3 style="color: #00E676; margin-bottom: 10px;">Navigation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation options with icons
    nav_options = {
        "Dashboard": {"icon": dashboard_icon, "desc": "Overview of your finances"},
        "Expenses": {"icon": expenses_icon, "desc": "Track and manage expenses"},
        "Budget": {"icon": budget_icon, "desc": "Set and monitor budgets"},
        "Insights": {"icon": insights_icon, "desc": "AI-powered financial insights"},
        "Goals": {"icon": goals_icon, "desc": "Track financial goals"}
    }
    
    # Create custom navigation buttons with icons
    for page, data in nav_options.items():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(data["icon"], unsafe_allow_html=True)
        with col2:
            if st.button(page, key=f"nav_{page}", use_container_width=True, 
                      help=data["desc"]):
                st.session_state.current_page = page
                st.rerun()
    
    selected_page = st.session_state.current_page
    
    # Display current date in sidebar with icon
    st.markdown("""<hr style="margin: 15px 0; border-color: rgba(255,255,255,0.1);">""", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(get_icon("calendar"), unsafe_allow_html=True)
    with col2:
        current_date = datetime.now().strftime("%B %d, %Y")
        st.markdown(f"<p style='margin: 0; color: #FFFFFF;'><strong>Today:</strong> {current_date}</p>", unsafe_allow_html=True)
    
    # Financial summary section with animations
    st.markdown("""
    <div style="margin-top: 20px; animation: fadeIn 1s ease-in-out;">
        <h3 style="color: #00E676; margin-bottom: 10px;">Financial Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate totals for sidebar display
    total_expenses = 0
    if st.session_state.expenses:
        total_expenses = sum(float(expense["amount"]) for expense in st.session_state.expenses)
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(get_icon("expenses"), unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <p style="margin: 0; color: #FFFFFF;"><strong>Total Expenses:</strong>
                <span style="color: #FF5252;">${total_expenses:.2f}</span>
            </p>
            """, unsafe_allow_html=True)
    
    # Show total budget with icon
    total_budget = 0
    if st.session_state.budgets:
        total_budget = sum(float(budget) for budget in st.session_state.budgets.values())
        
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(get_icon("budget"), unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <p style="margin: 0; color: #FFFFFF;"><strong>Total Budget:</strong>
                <span style="color: #00E676;">${total_budget:.2f}</span>
            </p>
            """, unsafe_allow_html=True)
        
        # Calculate remaining budget with visual indicator
        if st.session_state.expenses:
            remaining = total_budget - total_expenses
            
            col1, col2 = st.columns([1, 4])
            with col1:
                st.markdown(get_icon("money"), unsafe_allow_html=True)
            with col2:
                # Color code the remaining budget
                if remaining < 0:
                    color = "#FF5252"  # Red
                    icon = get_icon("alert")
                elif remaining < (total_budget * 0.2):
                    color = "#FFC107"  # Yellow/warning
                    icon = get_icon("warning")
                else:
                    color = "#00E676"  # Green
                    icon = get_icon("success")
                
                st.markdown(f"""
                <p style="margin: 0; color: #FFFFFF;"><strong>Remaining:</strong>
                    <span style="color: {color};">${remaining:.2f}</span>
                </p>
                """, unsafe_allow_html=True)
            
            # Add warning messages when budget is low or exceeded
            if remaining < 0:
                st.markdown(f"""
                <div style="margin-top: 10px; padding: 10px; border-radius: 5px; 
                          background-color: rgba(255, 82, 82, 0.1); border: 1px solid #FF5252;
                          animation: pulse 2s infinite;">
                    {get_icon("alert")}
                    <span style="color: #FF5252; margin-left: 5px;">You've exceeded your budget!</span>
                </div>
                """, unsafe_allow_html=True)
            elif remaining < (total_budget * 0.2):
                st.markdown(f"""
                <div style="margin-top: 10px; padding: 10px; border-radius: 5px; 
                          background-color: rgba(255, 193, 7, 0.1); border: 1px solid #FFC107;
                          animation: pulse 2s infinite;">
                    {get_icon("warning")}
                    <span style="color: #FFC107; margin-left: 5px;">Budget running low!</span>
                </div>
                """, unsafe_allow_html=True)
    
    # Data management section with animated icons
    st.markdown("""<hr style="margin: 15px 0; border-color: rgba(255,255,255,0.1);">""", unsafe_allow_html=True)
    st.markdown("""
    <div style="animation: fadeIn 1s ease-in-out;">
        <h3 style="color: #00E676; margin-bottom: 10px;">Data Management</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Export button with icon
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(get_icon("analysis"), unsafe_allow_html=True)
    with col2:
        if st.button("Export Data", key="export_data_button", use_container_width=True):
            # Export data from the database
            data = export_data()
            
            st.download_button(
                label="Download Finance Data",
                data=json.dumps(data, indent=2),
                file_name="finance_data.json",
                mime="application/json"
            )
            notification("Data ready for download!", "success")
    
    # Import data
    uploaded_file = st.file_uploader("Import saved data", type=["json"])
    if uploaded_file is not None:
        try:
            data = json.load(uploaded_file)
            # Import data to the database
            if import_data(data):
                # Refresh session state
                st.session_state.expenses = get_all_expenses()
                st.session_state.budgets = get_all_budgets()
                st.session_state.goals = get_all_goals()
                st.session_state.financial_insights = get_insights()
                notification("Data imported successfully!", "success")
                st.rerun()
        except Exception as e:
            notification(f"Error importing data: {e}", "error")
    
    # Information section
    st.markdown("""<hr style="margin: 15px 0; border-color: rgba(255,255,255,0.1);">""", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="padding: 15px; border-radius: 10px; 
              background-color: rgba(0, 230, 118, 0.1); 
              border: 1px solid rgba(0, 230, 118, 0.3);
              animation: fadeIn 1s ease-in-out, glow 3s infinite;
              margin-top: 15px;">
        {get_icon("info")}
        <p style="color: #FFFFFF; margin-top: 10px;">
            This is an AI-powered personal finance assistant. 
            Track expenses, set budgets, and get personalized financial insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Initialize authentication
initialize_auth()

# Check authentication
is_authenticated = clerk_auth()

# Handle authentication flow
if is_authenticated:
    # Show user profile in sidebar if authenticated
    with st.sidebar:
        st.markdown("""<hr style="margin: 15px 0; border-color: rgba(255,255,255,0.1);">""", unsafe_allow_html=True)
        st.markdown("""
        <div style="animation: fadeIn 1s ease-in-out;">
            <h3 style="color: #00E676; margin-bottom: 10px;">Your Profile</h3>
        </div>
        """, unsafe_allow_html=True)
        show_user_profile()
        logout_button()
    
    # Render selected page with animations
    pages[selected_page]()
    
    # Add footer
    display_footer()
else:
    # Show login page if not authenticated
    show_login_page()
