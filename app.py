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

# Import database utilities
from utils.database import (
    init_db, get_all_expenses, get_all_budgets, 
    get_all_goals, get_insights, export_data, import_data
)

# App configuration
st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .main .block-container {
        max-width: 100%;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    h1, h2, h3 {
        color: #4CAF50;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 0.3rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    .css-1aumxhk {
        background-color: #f1f8e9;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    /* Card-like styling for dataframes */
    .dataframe {
        border: none !important;
        border-radius: 0.5rem !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    .dataframe thead th {
        background-color: #e8f5e9 !important;
        color: #2e7d32 !important;
        font-weight: 600 !important;
    }
    .dataframe tbody tr:nth-child(even) {
        background-color: #f9f9f9 !important;
    }
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
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

# App title
st.sidebar.title("AI Finance Assistant")

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
        
        # Color code remaining budget
        if remaining < 0:
            st.sidebar.markdown(f"<span style='color:red'>You've exceeded your budget!</span>", unsafe_allow_html=True)
        elif remaining < (total_budget * 0.2):
            st.sidebar.markdown(f"<span style='color:orange'>Budget running low!</span>", unsafe_allow_html=True)

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

# Render selected page
pages[selected_page]()
