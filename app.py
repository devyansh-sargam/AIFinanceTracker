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

# App configuration
st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations and dark mode
st.markdown("""
<style>
    /* Dark mode & glow effects */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        animation: fadeIn 0.8s ease-in-out;
    }
    .main .block-container {
        max-width: 100%;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes glowing {
        0% { box-shadow: 0 0 5px rgba(0, 230, 118, 0.5); }
        50% { box-shadow: 0 0 20px rgba(0, 230, 118, 0.8); }
        100% { box-shadow: 0 0 5px rgba(0, 230, 118, 0.5); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Headings with glow */
    h1, h2, h3 {
        color: #00E676 !important;
        text-shadow: 0 0 10px rgba(0, 230, 118, 0.5);
        animation: fadeIn 1s ease-in-out;
    }
    
    /* Button styling with glow and animation */
    .stButton>button {
        background-color: #00E676 !important;
        color: #121212 !important;
        font-weight: bold !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 0.3rem !important;
        transition: all 0.3s !important;
        animation: glowing 2s infinite !important;
    }
    
    .stButton>button:hover {
        background-color: #00C853 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.8) !important;
    }
    
    /* Card styling */
    .css-1aumxhk, div.stDataFrame, div.stMarkdown {
        background-color: #1E1E1E !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        border: 1px solid #333333 !important;
        animation: fadeIn 0.5s ease-in-out;
        transition: all 0.3s ease;
    }
    
    .css-1aumxhk:hover, div.stDataFrame:hover {
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.3) !important;
        transform: translateY(-2px);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        border-right: 1px solid #333333 !important;
    }
    
    section[data-testid="stSidebar"] .block-container {
        animation: slideIn 0.5s ease-in-out;
    }
    
    /* Navigation */
    div.stRadio > div {
        background-color: #1E1E1E !important;
        border-radius: 5px !important;
        padding: 0.5rem !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.3s ease;
    }
    
    div.stRadio > div:hover {
        background-color: #2a2a2a !important;
        box-shadow: 0 0 10px rgba(0, 230, 118, 0.3) !important;
    }
    
    /* Card-like styling for dataframes */
    .dataframe {
        border: none !important;
        border-radius: 0.5rem !important;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2) !important;
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        animation: fadeIn 0.8s ease-in-out;
    }
    
    .dataframe thead th {
        background-color: #2a2a2a !important;
        color: #00E676 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #00E676 !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #252525 !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #333333 !important;
    }
    
    /* Progress bar styling with animation */
    .stProgress > div > div > div > div {
        background-color: #00E676 !important;
        background: linear-gradient(90deg, #00E676, #00C853) !important;
        animation: pulse 2s infinite !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stDateInput > div > div > input {
        background-color: #2a2a2a !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 5px !important;
    }
    
    .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus, .stDateInput > div > div > input:focus {
        border: 1px solid #00E676 !important;
        box-shadow: 0 0 10px rgba(0, 230, 118, 0.3) !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div > div {
        background-color: #2a2a2a !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
    }
    
    /* Plots and charts */
    .js-plotly-plot, .plotly, .plot-container {
        animation: fadeIn 1s ease-in-out;
    }
    
    /* Info boxes */
    div.stInfo {
        background-color: rgba(0, 230, 118, 0.1) !important;
        border: 1px solid #00E676 !important;
        border-radius: 10px !important;
        animation: glowing 3s infinite !important;
    }
    
    /* Warning/Error colors */
    .red-text {
        color: #FF5252 !important;
        text-shadow: 0 0 10px rgba(255, 82, 82, 0.5);
    }
    
    .yellow-text {
        color: #FFD740 !important;
        text-shadow: 0 0 10px rgba(255, 215, 64, 0.5);
    }
</style>
""", unsafe_allow_html=True)

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

# App title with animation and glow effect
st.sidebar.markdown("""
<div style="animation: fadeIn 1.5s ease-in-out;">
    <h1 style="color: #00E676; text-shadow: 0 0 15px rgba(0, 230, 118, 0.8); margin-bottom: 0.5rem;">
        <span style="display: inline-block; animation: pulse 2s infinite;">💰</span> 
        AI Finance Assistant
    </h1>
    <p style="color: rgba(255,255,255,0.8); font-style: italic; margin-top: 0;">Your smart money manager</p>
</div>
""", unsafe_allow_html=True)

# Navigation
pages = {
    "Dashboard": show_dashboard,
    "Expenses": show_expenses,
    "Budget": show_budget,
    "Insights": show_insights,
    "Goals": show_goals
}

# Sidebar navigation
st.sidebar.markdown("## Navigation")
selected_page = st.sidebar.radio("Go to", list(pages.keys()))
st.session_state.current_page = selected_page

# Display current date in sidebar
st.sidebar.markdown("---")
current_date = datetime.now().strftime("%B %d, %Y")
st.sidebar.markdown(f"**Today:** {current_date}")

# Calculate totals for sidebar display
total_expenses = 0
if st.session_state.expenses:
    total_expenses = sum(float(expense["amount"]) for expense in st.session_state.expenses)
    st.sidebar.markdown(f"**Total Expenses:** ${total_expenses:.2f}")

# Show total budget
total_budget = 0
if st.session_state.budgets:
    total_budget = sum(float(budget) for budget in st.session_state.budgets.values())
    st.sidebar.markdown(f"**Total Budget:** ${total_budget:.2f}")
    
    # Calculate remaining budget
    if st.session_state.expenses:
        remaining = total_budget - total_expenses
        st.sidebar.markdown(f"**Remaining Budget:** ${remaining:.2f}")
        
        # Color code remaining budget with glow effects
        if remaining < 0:
            st.sidebar.markdown(f"<span class='red-text' style='animation: pulse 2s infinite;'>⚠️ You've exceeded your budget!</span>", unsafe_allow_html=True)
        elif remaining < (total_budget * 0.2):
            st.sidebar.markdown(f"<span class='yellow-text' style='animation: pulse 2s infinite;'>⚠️ Budget running low!</span>", unsafe_allow_html=True)

# Link to save/load data
st.sidebar.markdown("---")
st.sidebar.markdown("### Data Management")

# Save data functionality
if st.sidebar.button("Export Data"):
    # Export data from the database
    data = export_data()
    
    st.sidebar.download_button(
        label="Download Finance Data",
        data=json.dumps(data, indent=2),
        file_name="finance_data.json",
        mime="application/json"
    )
    st.sidebar.success("Data ready for download!")

# Load data functionality
uploaded_file = st.sidebar.file_uploader("Import saved data", type=["json"])
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
            st.sidebar.success("Data imported successfully!")
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"Error importing data: {e}")

# Information
st.sidebar.markdown("---")
st.sidebar.info("This is an AI-powered personal finance assistant. Track expenses, set budgets, and get personalized financial insights.")

# Initialize authentication
initialize_auth()

# Check authentication
is_authenticated = clerk_auth()

# Handle authentication flow
if is_authenticated:
    # Show user profile in sidebar if authenticated
    st.sidebar.markdown("### Your Profile")
    show_user_profile()
    logout_button()
    
    # Render selected page
    pages[selected_page]()
else:
    # Show login page if not authenticated
    show_login_page()
