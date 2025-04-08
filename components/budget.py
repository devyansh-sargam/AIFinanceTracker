import streamlit as st
import pandas as pd
from datetime import datetime

from utils.openai_utils import get_budget_recommendations
from utils.data_utils import calculate_budget_progress, get_expenses_by_category, get_this_month_expenses
from utils.visualization import create_budget_progress_chart

def show_budget():
    """
    Display the budget management page.
    """
    st.title("Budget Management")
    
    # Create tabs for Set Budget and View Budget
    tab1, tab2 = st.tabs(["Set Budget", "View Budget"])
    
    with tab1:
        show_budget_form()
    
    with tab2:
        show_budget_progress()

def show_budget_form():
    """
    Display the form for setting budget amounts by category.
    """
    st.subheader("Set Monthly Budget")
    
    # Check if there are enough expenses for AI recommendations
    has_enough_data = len(st.session_state.expenses) >= 5
    
    # Allow AI to suggest budgets if enough data is available
    if has_enough_data:
        if st.button("Get AI Budget Recommendations"):
            with st.spinner("Analyzing your spending patterns..."):
                budget_recommendations = get_budget_recommendations(st.session_state.expenses)
                
                if budget_recommendations:
                    st.session_state.budgets = budget_recommendations
                    st.success("Budget recommendations generated! Review and adjust as needed.")
                    st.rerun()
                else:
                    st.error("Could not generate budget recommendations. Try again later.")
    else:
        st.info("Add at least 5 expenses to get AI budget recommendations.")
    
    # Get categories from expenses and add any missing default categories
    categories = set(expense["category"] for expense in st.session_state.expenses) if st.session_state.expenses else set()
    default_categories = {"Housing", "Transportation", "Food", "Entertainment", "Shopping", "Health", "Education", "Other"}
    all_categories = sorted(list(categories.union(default_categories)))
    
    # Create a form for setting budgets
    with st.form("budget_form"):
        st.markdown("Set your monthly budget for each category:")
        
        # Create budget inputs for each category
        budget_values = {}
        cols = st.columns(2)
        
        for i, category in enumerate(all_categories):
            col_idx = i % 2
            with cols[col_idx]:
                # Get existing budget value if available
                current_value = st.session_state.budgets.get(category, 0)
                
                # Create input field
                budget_values[category] = st.number_input(
                    f"{category} Budget ($)",
                    min_value=0.0,
                    value=float(current_value),
                    step=50.0,
                    format="%.2f",
                    key=f"budget_{category}"
                )
        
        # Submit button
        submitted = st.form_submit_button("Save Budget")
        
        if submitted:
            # Filter out zero budgets
            st.session_state.budgets = {
                category: str(amount) for category, amount in budget_values.items() if amount > 0
            }
            
            # Show success message
            st.success("Budget updated successfully!")
            
            # Show total budget
            total_budget = sum(float(amount) for amount in st.session_state.budgets.values())
            st.markdown(f"**Total Monthly Budget:** ${total_budget:.2f}")

def show_budget_progress():
    """
    Display budget progress and comparisons.
    """
    if not st.session_state.budgets:
        st.info("No budgets set yet. Use the 'Set Budget' tab to create your first budget.")
        return
    
    # Calculate budget progress
    budget_progress = calculate_budget_progress(st.session_state.expenses, st.session_state.budgets)
    
    # Show budget chart
    st.subheader("Budget Progress")
    st.plotly_chart(
        create_budget_progress_chart(st.session_state.expenses, st.session_state.budgets),
        use_container_width=True
    )
    
    # Budget details table
    st.subheader("Budget Details")
    
    # Create a table with budget details
    budget_data = []
    for category, data in budget_progress.items():
        budget_data.append({
            "Category": category,
            "Budget": f"${data['budget']:.2f}",
            "Spent": f"${data['spent']:.2f}",
            "Remaining": f"${data['remaining']:.2f}",
            "% Used": f"{data['percentage']:.1f}%",
            "Status": "Over Budget" if data['remaining'] < 0 else "On Track"
        })
    
    # Convert to dataframe and display
    if budget_data:
        df = pd.DataFrame(budget_data)
        
        # Highlight over budget items
        def highlight_over_budget(val):
            if val == "Over Budget":
                return 'background-color: #ffcccb'
            return ''
        
        st.dataframe(df.style.applymap(highlight_over_budget, subset=['Status']))
    else:
        st.info("No budget progress to display.")
    
    # Budget summary
    st.subheader("Budget Summary")
    
    # Calculate totals
    total_budget = sum(float(budget) for budget in st.session_state.budgets.values())
    total_spent = sum(data["spent"] for data in budget_progress.values())
    total_remaining = total_budget - total_spent
    percentage_used = (total_spent / total_budget * 100) if total_budget > 0 else 0
    
    # Display in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Budget", f"${total_budget:.2f}")
    
    with col2:
        st.metric("Total Spent", f"${total_spent:.2f}")
    
    with col3:
        st.metric("Remaining", f"${total_remaining:.2f}")
    
    with col4:
        st.metric("Budget Used", f"{percentage_used:.1f}%")
    
    # Budget tips
    st.markdown("---")
    st.subheader("Budget Tips")
    
    # Provide tips based on budget status
    if total_remaining < 0:
        st.error("You're over your total budget! Consider reducing spending in some categories.")
    elif total_remaining < (total_budget * 0.1):
        st.warning("You're close to your budget limit. Monitor your spending carefully for the rest of the month.")
    else:
        st.success("You're on track with your budget. Keep up the good work!")
    
    # Category-specific tips
    over_budget_categories = [category for category, data in budget_progress.items() if data["remaining"] < 0]
    
    if over_budget_categories:
        st.markdown("### Areas to Watch")
        for category in over_budget_categories:
            data = budget_progress[category]
            over_by = abs(data["remaining"])
            st.markdown(f"- **{category}**: Over budget by ${over_by:.2f} ({data['percentage']:.1f}% used)")
