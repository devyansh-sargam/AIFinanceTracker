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

# App configuration
st.set_page_config(
    page_title="AI Finance Assistant",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state.expenses = []
    
if "budgets" not in st.session_state:
    st.session_state.budgets = {}
    
if "goals" not in st.session_state:
    st.session_state.goals = []
    
if "financial_insights" not in st.session_state:
    st.session_state.financial_insights = []
    
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

# Display total expenses and budgets in sidebar
if st.session_state.expenses:
    total_expenses = sum(float(expense["amount"]) for expense in st.session_state.expenses)
    st.sidebar.markdown(f"**Total Expenses:** ${total_expenses:.2f}")

# Show total budget
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
if st.sidebar.button("Save Data"):
    data = {
        "expenses": st.session_state.expenses,
        "budgets": st.session_state.budgets,
        "goals": st.session_state.goals,
        "insights": st.session_state.financial_insights
    }
    
    st.sidebar.download_button(
        label="Download Finance Data",
        data=json.dumps(data, indent=2),
        file_name="finance_data.json",
        mime="application/json"
    )
    st.sidebar.success("Data ready for download!")

# Load data functionality
uploaded_file = st.sidebar.file_uploader("Upload saved data", type=["json"])
if uploaded_file is not None:
    try:
        data = json.load(uploaded_file)
        st.session_state.expenses = data.get("expenses", [])
        st.session_state.budgets = data.get("budgets", {})
        st.session_state.goals = data.get("goals", [])
        st.session_state.financial_insights = data.get("insights", [])
        st.sidebar.success("Data loaded successfully!")
    except Exception as e:
        st.sidebar.error(f"Error loading data: {e}")

# Information
st.sidebar.markdown("---")
st.sidebar.info("This is an AI-powered personal finance assistant. Track expenses, set budgets, and get personalized financial insights.")

# Render selected page
pages[selected_page]()
