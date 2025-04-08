import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

from utils.openai_utils import categorize_expense, analyze_spending_patterns
from utils.data_utils import get_expense_dataframe, get_expenses_by_category
from utils.visualization import create_spending_by_category_chart, create_category_comparison_chart

def show_expenses():
    """
    Display the expenses management page.
    """
    st.title("Expense Tracker")
    
    # Create tabs for Add Expense and View Expenses
    tab1, tab2 = st.tabs(["Add Expense", "View Expenses"])
    
    with tab1:
        show_add_expense_form()
    
    with tab2:
        show_expense_list()

def show_add_expense_form():
    """
    Display the form for adding a new expense.
    """
    st.subheader("Add New Expense")
    
    # Create a form for adding expenses
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            description = st.text_input("Description", placeholder="e.g., Grocery shopping")
            amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
            
        with col2:
            date = st.date_input("Date", datetime.now())
            
            # Option to manually set category or use AI
            use_ai_category = st.checkbox("Use AI to categorize", value=True)
            
            if not use_ai_category:
                category_options = [
                    "Housing", "Transportation", "Food", "Entertainment", 
                    "Shopping", "Health", "Education", "Travel", 
                    "Savings/Investment", "Other"
                ]
                category = st.selectbox("Category", category_options)
            else:
                category = "AI will categorize"
        
        # Submit button
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            if use_ai_category:
                with st.spinner("AI is categorizing your expense..."):
                    category = categorize_expense(description, amount)
            
            # Create new expense entry
            new_expense = {
                "description": description,
                "amount": str(amount),  # Store as string for consistent serialization
                "date": date.strftime("%Y-%m-%d"),
                "category": category
            }
            
            # Add to session state
            st.session_state.expenses.append(new_expense)
            
            # Update AI insights if we have enough data
            if len(st.session_state.expenses) >= 5:
                with st.spinner("Analyzing spending patterns..."):
                    st.session_state.financial_insights = analyze_spending_patterns(st.session_state.expenses)
            
            st.success(f"Added expense: {description} (${amount:.2f}) in {category} category")
            
            # Clear the form (need to rerun)
            st.rerun()

def show_expense_list():
    """
    Display the list of expenses with filtering and visualization.
    """
    if not st.session_state.expenses:
        st.info("No expenses recorded yet. Add your first expense using the form.")
        return
    
    # Filters section
    with st.expander("Filters", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Date range filter
            start_date = st.date_input("Start Date", datetime.now() - pd.Timedelta(days=30))
            end_date = st.date_input("End Date", datetime.now())
            
        with col2:
            # Category filter
            categories = ["All"] + list(set(expense["category"] for expense in st.session_state.expenses))
            selected_category = st.selectbox("Category", categories)
            
        with col3:
            # Amount range filter
            min_amount = st.number_input("Min Amount", min_value=0.0, step=10.0)
            max_amount = st.number_input("Max Amount", min_value=0.0, step=10.0, value=1000.0)
    
    # Apply filters
    filtered_expenses = st.session_state.expenses.copy()
    
    # Date filter
    filtered_expenses = [
        expense for expense in filtered_expenses
        if start_date.strftime("%Y-%m-%d") <= expense["date"] <= end_date.strftime("%Y-%m-%d")
    ]
    
    # Category filter
    if selected_category != "All":
        filtered_expenses = [
            expense for expense in filtered_expenses
            if expense["category"] == selected_category
        ]
    
    # Amount filter
    if min_amount > 0 or max_amount < 1000:
        filtered_expenses = [
            expense for expense in filtered_expenses
            if min_amount <= float(expense["amount"]) <= max_amount
        ]
    
    # Sort expenses by date (most recent first)
    filtered_expenses = sorted(
        filtered_expenses,
        key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),
        reverse=True
    )
    
    # Display summary
    st.subheader("Expense Summary")
    
    # Total in filtered view
    filtered_total = sum(float(expense["amount"]) for expense in filtered_expenses)
    st.markdown(f"**Total in current view:** ${filtered_total:.2f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            create_spending_by_category_chart(filtered_expenses),
            use_container_width=True
        )
    
    with col2:
        st.plotly_chart(
            create_category_comparison_chart(filtered_expenses),
            use_container_width=True
        )
    
    # Expense table with pagination
    st.subheader("Expense List")
    
    # Convert to dataframe for display
    if filtered_expenses:
        df = pd.DataFrame(filtered_expenses)
        df = df[["date", "description", "category", "amount"]]
        df.columns = ["Date", "Description", "Category", "Amount"]
        df["Amount"] = df["Amount"].apply(lambda x: f"${float(x):.2f}")
        
        # Pagination
        page_size = 10
        total_pages = (len(df) + page_size - 1) // page_size
        
        if "expense_page" not in st.session_state:
            st.session_state.expense_page = 0
        
        # Page navigation
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            if st.button("Previous", disabled=st.session_state.expense_page <= 0):
                st.session_state.expense_page -= 1
                st.rerun()
        
        with col2:
            if total_pages > 0:
                st.markdown(f"**Page {st.session_state.expense_page + 1} of {total_pages}**")
            else:
                st.markdown("**Page 1 of 1**")
        
        with col3:
            if st.button("Next", disabled=st.session_state.expense_page >= total_pages - 1):
                st.session_state.expense_page += 1
                st.rerun()
        
        # Display current page
        start_idx = st.session_state.expense_page * page_size
        end_idx = min(start_idx + page_size, len(df))
        st.table(df.iloc[start_idx:end_idx])
        
        # Delete expenses
        st.subheader("Delete Expenses")
        expense_to_delete = st.selectbox(
            "Select expense to delete",
            [f"{e['date']} - {e['description']} - ${float(e['amount']):.2f}" for e in st.session_state.expenses]
        )
        
        if st.button("Delete Selected Expense", type="primary"):
            # Find the expense to delete
            index_to_delete = [
                f"{e['date']} - {e['description']} - ${float(e['amount']):.2f}" 
                for e in st.session_state.expenses
            ].index(expense_to_delete)
            
            # Remove it
            st.session_state.expenses.pop(index_to_delete)
            st.success("Expense deleted successfully!")
            st.rerun()
    else:
        st.info("No expenses match the current filters.")
