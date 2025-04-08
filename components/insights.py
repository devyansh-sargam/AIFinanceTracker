import streamlit as st
import pandas as pd
from datetime import datetime

from utils.openai_utils import analyze_spending_patterns, get_saving_recommendations
from utils.data_utils import get_expense_dataframe, get_expenses_by_category
from utils.visualization import create_spending_by_category_chart, create_spending_over_time_chart, create_category_comparison_chart

def show_insights():
    """
    Display AI-powered financial insights and recommendations.
    """
    st.title("Financial Insights")
    
    # Check if there are enough expenses for analysis
    if not st.session_state.expenses or len(st.session_state.expenses) < 3:
        st.info("Add at least 3 expenses to receive AI-powered financial insights.")
        return
    
    # Add a button to refresh insights
    if st.button("Generate New Insights"):
        with st.spinner("Analyzing your financial data..."):
            # Get spending pattern insights
            st.session_state.financial_insights = analyze_spending_patterns(st.session_state.expenses)
            
            # Get saving recommendations
            if st.session_state.budgets:
                st.session_state.saving_recommendations = get_saving_recommendations(
                    st.session_state.expenses, 
                    st.session_state.budgets
                )
            else:
                st.session_state.saving_recommendations = [
                    "Set up budgets to receive personalized saving recommendations."
                ]
                
        st.success("Insights generated successfully!")
        st.rerun()
    
    # Display the insights
    st.subheader("Spending Pattern Analysis")
    
    if "financial_insights" in st.session_state and st.session_state.financial_insights:
        for i, insight in enumerate(st.session_state.financial_insights):
            st.markdown(f"💡 **Insight {i+1}:** {insight}")
    else:
        with st.spinner("Analyzing your spending patterns..."):
            st.session_state.financial_insights = analyze_spending_patterns(st.session_state.expenses)
            st.rerun()
    
    # Display saving recommendations
    st.subheader("Saving Recommendations")
    
    if "saving_recommendations" not in st.session_state:
        with st.spinner("Generating saving recommendations..."):
            if st.session_state.budgets:
                st.session_state.saving_recommendations = get_saving_recommendations(
                    st.session_state.expenses, 
                    st.session_state.budgets
                )
            else:
                st.session_state.saving_recommendations = [
                    "Set up budgets to receive personalized saving recommendations."
                ]
    
    for i, recommendation in enumerate(st.session_state.saving_recommendations):
        st.markdown(f"💰 **Tip {i+1}:** {recommendation}")
    
    # Display visualizations
    st.markdown("---")
    st.subheader("Visual Insights")
    
    # Category spending
    st.plotly_chart(
        create_spending_by_category_chart(st.session_state.expenses),
        use_container_width=True
    )
    
    # Spending over time
    st.plotly_chart(
        create_spending_over_time_chart(st.session_state.expenses, "month"),
        use_container_width=True
    )
    
    # Category comparison over time
    st.plotly_chart(
        create_category_comparison_chart(st.session_state.expenses),
        use_container_width=True
    )
    
    # Display top spending categories
    st.markdown("---")
    st.subheader("Top Spending Categories")
    
    # Calculate category totals
    category_totals = get_expenses_by_category(st.session_state.expenses)
    
    if category_totals:
        # Convert to dataframe and sort
        df = pd.DataFrame({
            "Category": list(category_totals.keys()),
            "Amount": list(category_totals.values())
        }).sort_values("Amount", ascending=False)
        
        # Add percentage column
        total = df["Amount"].sum()
        df["Percentage"] = (df["Amount"] / total * 100).round(1)
        
        # Format columns
        df["Amount"] = df["Amount"].apply(lambda x: f"${x:.2f}")
        df["Percentage"] = df["Percentage"].apply(lambda x: f"{x}%")
        
        # Display table
        st.table(df.head(5))
        
        # Display spending insights
        st.markdown("### Spending Breakdown")
        
        # Calculate some simple insights
        top_category = df.iloc[0]["Category"]
        top_percentage = df.iloc[0]["Percentage"]
        
        st.markdown(f"- Your highest spending category is **{top_category}** at {top_percentage} of total expenses.")
        
        # Display low spending categories
        if len(df) > 5:
            st.markdown("### Areas Where You Spend Less")
            bottom_categories = df.tail(3)["Category"].tolist()
            st.markdown(f"You spend relatively little on: **{', '.join(bottom_categories)}**")
    else:
        st.info("Add expenses to see your top spending categories.")
    
    # Financial health score
    st.markdown("---")
    st.subheader("Financial Health Assessment")
    
    # Only show if budgets are set
    if st.session_state.budgets:
        # Calculate basic financial health score (0-100)
        score = calculate_financial_health_score(st.session_state.expenses, st.session_state.budgets)
        
        # Display score
        st.markdown(f"### Your Financial Health Score: {score}/100")
        
        # Progress bar for score
        st.progress(score / 100)
        
        # Interpret score
        if score >= 80:
            st.success("Excellent! You're managing your finances very well.")
        elif score >= 60:
            st.info("Good job! Your finances are generally on track with some room for improvement.")
        elif score >= 40:
            st.warning("Your financial health needs attention in some areas.")
        else:
            st.error("Your financial health needs significant improvement. Consider following the recommendations above.")
    else:
        st.info("Set up budgets to see your financial health assessment.")

def calculate_financial_health_score(expenses, budgets):
    """
    Calculate a simple financial health score based on budget adherence.
    """
    # Initialize score
    score = 50  # Start at middle
    
    # Get monthly expenses
    df = get_expense_dataframe(expenses)
    if df.empty:
        return score
    
    # Add month column
    df["month"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m")
    
    # Get current month
    current_month = datetime.now().strftime("%Y-%m")
    
    # Filter to current month
    current_df = df[df["month"] == current_month]
    
    if current_df.empty:
        return score
    
    # Calculate budget adherence
    budget_total = sum(float(budget) for budget in budgets.values())
    monthly_expenses = current_df["amount"].sum()
    
    if budget_total > 0:
        # Budget adherence affects score (up to ±30 points)
        budget_ratio = monthly_expenses / budget_total
        if budget_ratio <= 1:
            # Under budget is good
            score += (1 - budget_ratio) * 30
        else:
            # Over budget reduces score
            score -= min(30, (budget_ratio - 1) * 50)  # Penalize more for being over budget
    
    # Check category distribution (balanced spending is good)
    category_totals = current_df.groupby("category")["amount"].sum()
    if len(category_totals) > 3:
        # More diverse categories is better
        score += min(10, len(category_totals) * 2)
    
    # Check for very high spending in a single category
    if not category_totals.empty:
        max_category_percent = (category_totals.max() / category_totals.sum()) * 100
        if max_category_percent > 50:
            # Penalize for having >50% spending in one category
            score -= min(15, (max_category_percent - 50) / 5)
    
    # Consistency in spending (less variation is better)
    if len(df["month"].unique()) > 1:
        monthly_totals = df.groupby("month")["amount"].sum()
        if len(monthly_totals) > 1:
            variation = monthly_totals.std() / monthly_totals.mean() if monthly_totals.mean() > 0 else 0
            if variation < 0.2:
                score += 10  # Low variation is good
            elif variation > 0.5:
                score -= 10  # High variation is concerning
    
    # Ensure score is between 0 and 100
    return max(0, min(100, int(score)))
