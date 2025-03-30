import pandas as pd
from datetime import datetime, timedelta
import calendar

def get_expense_dataframe(expenses):
    """
    Convert the expenses list to a pandas DataFrame.
    """
    if not expenses:
        return pd.DataFrame(columns=["date", "category", "description", "amount"])
    
    df = pd.DataFrame(expenses)
    # Convert date strings to datetime objects
    df["date"] = pd.to_datetime(df["date"])
    # Convert amount strings to float
    df["amount"] = df["amount"].astype(float)
    
    return df

def get_expenses_by_category(expenses):
    """
    Group expenses by category and calculate totals.
    """
    df = get_expense_dataframe(expenses)
    if df.empty:
        return {}
    
    grouped = df.groupby("category")["amount"].sum().to_dict()
    return grouped

def get_expenses_by_date(expenses, period="month"):
    """
    Group expenses by date (day, week, month, or year).
    """
    df = get_expense_dataframe(expenses)
    if df.empty:
        return {}
    
    if period == "day":
        df["period"] = df["date"].dt.date
    elif period == "week":
        df["period"] = df["date"].dt.to_period("W").apply(lambda x: x.start_time.date())
    elif period == "month":
        df["period"] = df["date"].dt.to_period("M").apply(lambda x: x.start_time.date())
    else:  # year
        df["period"] = df["date"].dt.to_period("Y").apply(lambda x: x.start_time.date())
    
    grouped = df.groupby("period")["amount"].sum().to_dict()
    # Convert keys back to strings
    grouped = {str(k): v for k, v in grouped.items()}
    
    return grouped

def get_this_month_expenses(expenses):
    """
    Filter expenses for the current month.
    """
    df = get_expense_dataframe(expenses)
    if df.empty:
        return []
    
    today = datetime.now()
    start_of_month = datetime(today.year, today.month, 1)
    end_of_month = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    
    monthly_df = df[(df["date"] >= start_of_month) & (df["date"] <= end_of_month)]
    return monthly_df.to_dict("records")

def get_monthly_breakdown(expenses):
    """
    Break down expenses by month and category.
    """
    df = get_expense_dataframe(expenses)
    if df.empty:
        return {}
    
    # Add month column
    df["month"] = df["date"].dt.to_period("M").astype(str)
    
    # Group by month and category
    result = {}
    for month, month_df in df.groupby("month"):
        result[month] = month_df.groupby("category")["amount"].sum().to_dict()
    
    return result

def calculate_budget_progress(expenses, budgets):
    """
    Calculate budget progress for each category.
    """
    if not budgets:
        return {}
    
    # Get monthly expenses by category
    monthly_expenses = get_expenses_by_category(get_this_month_expenses(expenses))
    
    # Calculate progress
    progress = {}
    for category, budget in budgets.items():
        spent = monthly_expenses.get(category, 0)
        budget_float = float(budget)
        
        if budget_float > 0:
            percentage = (spent / budget_float) * 100
        else:
            percentage = 0
            
        progress[category] = {
            "spent": spent,
            "budget": budget_float,
            "remaining": budget_float - spent,
            "percentage": min(percentage, 100)  # Cap at 100%
        }
    
    return progress

def filter_expenses(expenses, start_date=None, end_date=None, category=None, min_amount=None, max_amount=None):
    """
    Filter expenses based on various criteria.
    """
    df = get_expense_dataframe(expenses)
    if df.empty:
        return []
    
    # Apply filters
    if start_date:
        start_date = pd.to_datetime(start_date)
        df = df[df["date"] >= start_date]
    
    if end_date:
        end_date = pd.to_datetime(end_date)
        df = df[df["date"] <= end_date]
    
    if category and category != "All":
        df = df[df["category"] == category]
    
    if min_amount is not None:
        df = df[df["amount"] >= float(min_amount)]
    
    if max_amount is not None:
        df = df[df["amount"] <= float(max_amount)]
    
    return df.to_dict("records")
