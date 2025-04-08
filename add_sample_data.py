"""
Add sample data to the Finance Assistant database.
"""
import json
from datetime import datetime, timedelta
from utils.database import (
    add_expense, save_budget, add_goal, save_insights,
    get_all_expenses, get_all_budgets, get_all_goals, get_insights
)

def add_sample_expenses():
    """Add sample expenses to the database."""
    # Get current expenses
    current_expenses = get_all_expenses()
    if current_expenses:
        print("Expenses already exist. Skipping sample expense creation.")
        return
    
    # Create sample expenses over the last 2 months
    today = datetime.now().date()
    
    # Sample expense descriptions by category
    expense_samples = {
        "Housing": [
            {"desc": "Rent payment", "amount": 1200},
            {"desc": "Electricity bill", "amount": 85},
            {"desc": "Water bill", "amount": 45},
            {"desc": "Internet service", "amount": 65},
        ],
        "Food": [
            {"desc": "Grocery shopping", "amount": 120},
            {"desc": "Restaurant dinner", "amount": 45},
            {"desc": "Coffee shop", "amount": 5},
            {"desc": "Food delivery", "amount": 30},
        ],
        "Transportation": [
            {"desc": "Gas fillup", "amount": 40},
            {"desc": "Car insurance", "amount": 90},
            {"desc": "Uber ride", "amount": 15},
            {"desc": "Public transit pass", "amount": 75},
        ],
        "Entertainment": [
            {"desc": "Movie tickets", "amount": 25},
            {"desc": "Streaming subscription", "amount": 15},
            {"desc": "Concert tickets", "amount": 80},
            {"desc": "Video game purchase", "amount": 60},
        ],
        "Shopping": [
            {"desc": "New shoes", "amount": 70},
            {"desc": "Clothes shopping", "amount": 100},
            {"desc": "Electronics purchase", "amount": 200},
            {"desc": "Home decor", "amount": 50},
        ],
        "Health": [
            {"desc": "Gym membership", "amount": 40},
            {"desc": "Pharmacy purchase", "amount": 25},
            {"desc": "Doctor visit copay", "amount": 30},
            {"desc": "Vitamin supplements", "amount": 20},
        ],
    }
    
    # Add expenses for the past 60 days with some variability
    expenses_added = 0
    for days_ago in range(60, -1, -1):
        expense_date = today - timedelta(days=days_ago)
        
        # Add 0-3 expenses for each day
        for _ in range(min(3, days_ago % 4)):
            # Choose a category based on the day of the month
            categories = list(expense_samples.keys())
            category_idx = (days_ago + expenses_added) % len(categories)
            category = categories[category_idx]
            
            # Choose an expense from the category
            expense_options = expense_samples[category]
            expense_idx = (days_ago + expenses_added) % len(expense_options)
            expense = expense_options[expense_idx]
            
            # Add some variability to amounts
            amount_variation = 0.9 + (days_ago % 3) * 0.1  # 0.9 to 1.1
            
            # Create the expense
            expense_data = {
                "description": expense["desc"],
                "amount": str(round(expense["amount"] * amount_variation, 2)),
                "date": expense_date.strftime("%Y-%m-%d"),
                "category": category
            }
            
            add_expense(expense_data)
            expenses_added += 1
    
    print(f"Added {expenses_added} sample expenses")

def add_sample_budgets():
    """Add sample budgets to the database."""
    # Get current budgets
    current_budgets = get_all_budgets()
    if current_budgets:
        print("Budgets already exist. Skipping sample budget creation.")
        return
    
    # Create sample budgets
    sample_budgets = {
        "Housing": 1500,
        "Food": 500,
        "Transportation": 300,
        "Entertainment": 200,
        "Shopping": 300,
        "Health": 150,
        "Savings/Investment": 400,
        "Education": 100,
        "Travel": 200,
        "Other": 100
    }
    
    for category, amount in sample_budgets.items():
        save_budget(category, amount)
    
    print(f"Added {len(sample_budgets)} sample budgets")

def add_sample_goals():
    """Add sample financial goals to the database."""
    # Get current goals
    current_goals = get_all_goals()
    if current_goals:
        print("Goals already exist. Skipping sample goal creation.")
        return
    
    # Today's date for reference
    today = datetime.now().date()
    
    # Create sample goals
    sample_goals = [
        {
            "name": "Emergency Fund",
            "target_amount": "5000",
            "current_amount": "2500",
            "target_date": (today + timedelta(days=180)).strftime("%Y-%m-%d"),
            "priority": "High",
            "notes": "Build a 3-month emergency fund for unexpected expenses",
            "progress_updates": [
                {"date": (today - timedelta(days=60)).strftime("%Y-%m-%d"), "amount": "1000", "notes": "Initial deposit"},
                {"date": (today - timedelta(days=30)).strftime("%Y-%m-%d"), "amount": "1500", "notes": "Monthly contribution"}
            ]
        },
        {
            "name": "New Car Down Payment",
            "target_amount": "8000",
            "current_amount": "1200",
            "target_date": (today + timedelta(days=365)).strftime("%Y-%m-%d"),
            "priority": "Medium",
            "notes": "Save for 20% down payment on a reliable used car",
            "progress_updates": [
                {"date": (today - timedelta(days=90)).strftime("%Y-%m-%d"), "amount": "500", "notes": "Initial savings"},
                {"date": (today - timedelta(days=60)).strftime("%Y-%m-%d"), "amount": "700", "notes": "Tax refund"}
            ]
        },
        {
            "name": "Vacation Fund",
            "target_amount": "3000",
            "current_amount": "800",
            "target_date": (today + timedelta(days=120)).strftime("%Y-%m-%d"),
            "priority": "Low",
            "notes": "Summer vacation to the beach",
            "progress_updates": [
                {"date": (today - timedelta(days=45)).strftime("%Y-%m-%d"), "amount": "500", "notes": "Birthday money"},
                {"date": (today - timedelta(days=15)).strftime("%Y-%m-%d"), "amount": "300", "notes": "Side gig income"}
            ]
        },
        {
            "name": "Home Renovation",
            "target_amount": "10000",
            "current_amount": "2000",
            "target_date": (today + timedelta(days=730)).strftime("%Y-%m-%d"),
            "priority": "Medium",
            "notes": "Kitchen remodel project",
            "progress_updates": [
                {"date": (today - timedelta(days=120)).strftime("%Y-%m-%d"), "amount": "1000", "notes": "Bonus from work"},
                {"date": (today - timedelta(days=60)).strftime("%Y-%m-%d"), "amount": "1000", "notes": "Monthly contributions"}
            ]
        }
    ]
    
    for goal_data in sample_goals:
        add_goal(goal_data)
    
    print(f"Added {len(sample_goals)} sample goals")

def add_sample_insights():
    """Add sample financial insights to the database."""
    # Get current insights
    current_insights = get_insights()
    if current_insights:
        print("Insights already exist. Skipping sample insight creation.")
        return
    
    # Create sample insights
    sample_insights = [
        "You've spent 15% less on Food this month compared to last month. Great job reducing your restaurant expenses!",
        "Your Transportation costs have increased by 12% this month. Consider carpooling or using public transit more often.",
        "You're consistently staying under budget in the Entertainment category. Consider reallocating some of this budget to your Emergency Fund goal.",
        "Your Emergency Fund is now 50% funded! At your current saving rate, you'll reach your goal 2 weeks ahead of schedule.",
        "Tip: Setting up automatic transfers to your savings account can help you reach your financial goals faster.",
        "Your average daily spending this month is $42, which is 8% lower than last month."
    ]
    
    save_insights(sample_insights)
    print(f"Added {len(sample_insights)} sample insights")

if __name__ == "__main__":
    print("Adding sample data to the database...")
    add_sample_expenses()
    add_sample_budgets()
    add_sample_goals()
    add_sample_insights()
    print("Sample data added successfully!")