import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

from utils.data_utils import get_expense_dataframe, get_expenses_by_category, calculate_budget_progress, get_this_month_expenses
from utils.visualization import create_spending_by_category_chart, create_spending_over_time_chart, create_budget_progress_chart

def show_dashboard():
    """
    Display the main dashboard with financial overview.
    """
    st.title("Financial Dashboard")
    
    # Check if there are any expenses
    if not st.session_state.expenses:
        st.info("Welcome to your AI Finance Assistant! Get started by adding expenses in the Expenses section.")
        
        # Quick start buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Add Expense"):
                st.session_state.current_page = "Expenses"
                st.rerun()
                
        with col2:
            if st.button("Set Budget"):
                st.session_state.current_page = "Budget"
                st.rerun()
                
        with col3:
            if st.button("Set Financial Goal"):
                st.session_state.current_page = "Goals"
                st.rerun()
        
        # Display sample dashboard image
        st.markdown("### Your dashboard will look something like this once you add data:")
        # Use Streamlit markdown to describe what will be shown
        st.markdown("""
        📊 **Dashboard Features:**
        - Spending by category visualization
        - Monthly expense tracking
        - Budget progress bars
        - Recent transactions list
        - Financial insights powered by AI
        
        Start tracking your finances today by adding your first expense!
        """)
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate total expenses
    total_expenses = sum(float(expense["amount"]) for expense in st.session_state.expenses)
    
    # Calculate this month's expenses
    this_month_expenses = get_this_month_expenses(st.session_state.expenses)
    month_total = sum(float(expense["amount"]) for expense in this_month_expenses)
    
    # Get today's date
    today = datetime.now()
    current_month = today.strftime("%B %Y")
    
    # Calculate daily average for this month
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_passed = min(today.day, days_in_month)
    daily_avg = month_total / days_passed if days_passed > 0 else 0
    
    # Display enhanced metrics with animations and effects
    with col1:
        # Total Expenses Card
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-shimmer"></div>
            <div class="metric-card-content">
                <div class="metric-label">Total Expenses</div>
                <div class="metric-value">${total_expenses:.2f}</div>
            </div>
            <div class="metric-icon">💰</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Monthly Expenses Card
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-shimmer"></div>
            <div class="metric-card-content">
                <div class="metric-label">{current_month} Expenses</div>
                <div class="metric-value">${month_total:.2f}</div>
            </div>
            <div class="metric-icon">📅</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Daily Average Card
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-card-shimmer"></div>
            <div class="metric-card-content">
                <div class="metric-label">Daily Average</div>
                <div class="metric-value">${daily_avg:.2f}</div>
            </div>
            <div class="metric-icon">📊</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Calculate remaining budget if budgets exist
        if st.session_state.budgets:
            total_budget = sum(float(budget) for budget in st.session_state.budgets.values())
            remaining = total_budget - month_total
            
            # Choose icon and color based on remaining amount
            if remaining < 0:
                icon = "⚠️"
                color_class = "danger"
            elif remaining < (total_budget * 0.2):
                icon = "⚠️"
                color_class = "warning"
            else:
                icon = "✅"
                color_class = "success"
                
            # Remaining Budget Card
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-shimmer"></div>
                <div class="metric-card-content">
                    <div class="metric-label">Remaining Budget</div>
                    <div class="metric-value">${remaining:.2f}</div>
                </div>
                <div class="metric-icon">{icon}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Transactions Card
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-card-shimmer"></div>
                <div class="metric-card-content">
                    <div class="metric-label">Transactions</div>
                    <div class="metric-value">{len(st.session_state.expenses)}</div>
                </div>
                <div class="metric-icon">🧾</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Charts section
    st.markdown("---")
    st.subheader("Financial Overview")
    
    # Two charts side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(
            create_spending_by_category_chart(this_month_expenses),
            use_container_width=True
        )
    
    with col2:
        time_period = st.selectbox(
            "Time Period",
            ["week", "month", "year"],
            index=1,
            key="time_period_selector"
        )
        st.plotly_chart(
            create_spending_over_time_chart(st.session_state.expenses, time_period),
            use_container_width=True
        )
    
    # Budget progress if budgets exist
    if st.session_state.budgets:
        st.markdown("---")
        st.subheader("Budget Progress")
        st.plotly_chart(
            create_budget_progress_chart(st.session_state.expenses, st.session_state.budgets),
            use_container_width=True
        )
    
    # Recent transactions
    st.markdown("---")
    st.subheader("Recent Transactions")
    
    # Sort expenses by date (most recent first)
    recent_expenses = sorted(
        st.session_state.expenses,
        key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"),
        reverse=True
    )[:5]  # Show only the 5 most recent
    
    if recent_expenses:
        # Create a table
        df = pd.DataFrame(recent_expenses)
        df = df[["date", "description", "category", "amount"]]
        df.columns = ["Date", "Description", "Category", "Amount"]
        df["Amount"] = df["Amount"].apply(lambda x: f"${float(x):.2f}")
        
        st.table(df)
    else:
        st.info("No recent transactions to display.")
    
    # AI-powered insights
    st.markdown("---")
    st.subheader("AI Financial Insights")
    
    # Check if we have insights
    if st.session_state.financial_insights:
        for idx, insight in enumerate(st.session_state.financial_insights):
            st.markdown(f"💡 {insight}")
    else:
        st.info("Add more transactions to receive AI-powered financial insights.")
