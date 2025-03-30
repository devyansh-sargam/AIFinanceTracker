import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import calendar
from utils.data_utils import get_expense_dataframe, get_expenses_by_category, get_expenses_by_date, calculate_budget_progress, get_this_month_expenses

def create_spending_by_category_chart(expenses):
    """
    Create a pie chart showing spending by category.
    """
    category_totals = get_expenses_by_category(expenses)
    
    if not category_totals:
        return go.Figure().update_layout(
            title="No expense data available",
            annotations=[dict(text="Add expenses to see spending by category", showarrow=False, xref="paper", yref="paper", x=0.5, y=0.5)]
        )
    
    # Create dataframe from category totals
    df = pd.DataFrame({
        "Category": list(category_totals.keys()),
        "Amount": list(category_totals.values())
    })
    
    fig = px.pie(
        df, 
        values="Amount", 
        names="Category",
        title="Spending by Category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    
    # Improve layout
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        margin=dict(t=50, b=100, l=10, r=10)
    )
    
    return fig

def create_spending_over_time_chart(expenses, period="month"):
    """
    Create a line chart showing spending over time.
    """
    time_totals = get_expenses_by_date(expenses, period)
    
    if not time_totals:
        return go.Figure().update_layout(
            title="No expense data available",
            annotations=[dict(text="Add expenses to see spending over time", showarrow=False, xref="paper", yref="paper", x=0.5, y=0.5)]
        )
    
    # Convert to dataframe
    df = pd.DataFrame({
        "Date": pd.to_datetime(list(time_totals.keys())),
        "Amount": list(time_totals.values())
    }).sort_values("Date")
    
    # Create line chart
    fig = px.line(
        df,
        x="Date",
        y="Amount",
        title=f"Spending Over Time (by {period})",
        markers=True
    )
    
    # Improve layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Amount ($)",
        hovermode="x unified"
    )
    
    return fig

def create_budget_progress_chart(expenses, budgets):
    """
    Create a progress bar chart showing budget utilization.
    """
    progress = calculate_budget_progress(expenses, budgets)
    
    if not progress:
        return go.Figure().update_layout(
            title="No budget data available",
            annotations=[dict(text="Set budgets to track your progress", showarrow=False, xref="paper", yref="paper", x=0.5, y=0.5)]
        )
    
    # Convert to dataframe
    categories = []
    spent_values = []
    remaining_values = []
    
    for category, data in progress.items():
        categories.append(category)
        spent_values.append(data["spent"])
        # Only show remaining if it's positive
        remaining_values.append(max(0, data["remaining"]))
    
    # Create figure
    fig = go.Figure()
    
    # Add spent bars
    fig.add_trace(go.Bar(
        name="Spent",
        y=categories,
        x=spent_values,
        orientation='h',
        marker_color='#1E88E5'
    ))
    
    # Add remaining bars
    fig.add_trace(go.Bar(
        name="Remaining",
        y=categories,
        x=remaining_values,
        orientation='h',
        marker_color='#80CBC4'
    ))
    
    # Update layout
    fig.update_layout(
        title="Budget Progress",
        barmode='stack',
        xaxis_title="Amount ($)",
        yaxis_title="Category",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=10, r=10, t=60, b=10),
    )
    
    return fig

def create_monthly_comparison_chart(expenses):
    """
    Create a bar chart comparing spending across months.
    """
    df = get_expense_dataframe(expenses)
    
    if df.empty:
        return go.Figure().update_layout(
            title="No expense data available",
            annotations=[dict(text="Add expenses to see monthly comparison", showarrow=False, xref="paper", yref="paper", x=0.5, y=0.5)]
        )
    
    # Add month column
    df["month"] = df["date"].dt.strftime("%Y-%m")
    
    # Group by month
    monthly_totals = df.groupby("month")["amount"].sum().reset_index()
    
    # Sort by month
    monthly_totals = monthly_totals.sort_values("month")
    
    # Create bar chart
    fig = px.bar(
        monthly_totals,
        x="month",
        y="amount",
        title="Monthly Spending Comparison",
        text_auto='.2s'
    )
    
    # Improve layout
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Total Spending ($)",
        xaxis=dict(tickangle=-45)
    )
    
    return fig

def create_category_comparison_chart(expenses):
    """
    Create a stacked bar chart showing category spending across months.
    """
    df = get_expense_dataframe(expenses)
    
    if df.empty:
        return go.Figure().update_layout(
            title="No expense data available",
            annotations=[dict(text="Add expenses to see category comparison", showarrow=False, xref="paper", yref="paper", x=0.5, y=0.5)]
        )
    
    # Add month column
    df["month"] = df["date"].dt.strftime("%Y-%m")
    
    # Group by month and category
    monthly_category = df.pivot_table(
        index="month", 
        columns="category", 
        values="amount", 
        aggfunc="sum"
    ).fillna(0).reset_index()
    
    # Sort by month
    monthly_category = monthly_category.sort_values("month")
    
    # Create stacked bar chart
    fig = px.bar(
        monthly_category,
        x="month",
        y=monthly_category.columns[1:],
        title="Category Spending by Month",
        labels={"value": "Amount ($)", "variable": "Category"},
    )
    
    # Improve layout
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        xaxis=dict(tickangle=-45),
        legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5)
    )
    
    return fig
