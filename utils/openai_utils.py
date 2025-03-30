import os
import json
from openai import OpenAI

# Initialize OpenAI client
# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def categorize_expense(description, amount):
    """
    Use OpenAI to categorize an expense based on its description.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """You are a financial assistant that categorizes expenses.
                Categorize the following expense into one of these categories:
                - Housing (rent, mortgage, utilities)
                - Transportation (car payments, gas, public transit)
                - Food (groceries, restaurants)
                - Entertainment (movies, games, streaming)
                - Shopping (clothes, electronics)
                - Health (medical bills, prescriptions)
                - Education (tuition, books)
                - Travel (flights, hotels)
                - Savings/Investment
                - Other
                
                Respond with ONLY the category name, nothing else."""},
                {"role": "user", "content": f"Description: {description}, Amount: ${amount}"}
            ],
            max_tokens=20
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error categorizing expense: {e}")
        return "Other"

def analyze_spending_patterns(expenses):
    """
    Analyze spending patterns and provide insights.
    """
    if not expenses or len(expenses) < 3:
        return "Not enough expense data to analyze patterns."
    
    expenses_text = "\n".join([f"Category: {e['category']}, Amount: ${e['amount']}, Date: {e['date']}, Description: {e['description']}" for e in expenses])
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """You are a financial advisor analyzing spending patterns.
                Provide 3-5 concise, actionable insights about spending patterns.
                Format your response as a JSON array of strings, each string being one insight.
                Be specific, practical, and focus on areas where the user could save money."""},
                {"role": "user", "content": f"Here are the recent expenses:\n{expenses_text}"}
            ],
            response_format={"type": "json_object"}
        )
        insights = json.loads(response.choices[0].message.content)
        return insights.get("insights", [])
    except Exception as e:
        print(f"Error analyzing spending patterns: {e}")
        return ["Unable to analyze spending patterns at this time."]

def get_saving_recommendations(expenses, budgets):
    """
    Generate personalized saving recommendations based on spending history and budgets.
    """
    if not expenses:
        return ["Start tracking your expenses to get personalized recommendations."]
    
    # Prepare the expense and budget data for the AI
    expenses_by_category = {}
    for expense in expenses:
        category = expense['category']
        amount = float(expense['amount'])
        if category in expenses_by_category:
            expenses_by_category[category] += amount
        else:
            expenses_by_category[category] = amount
    
    expense_summary = "\n".join([f"- {category}: ${amount:.2f}" for category, amount in expenses_by_category.items()])
    budget_summary = "\n".join([f"- {category}: ${amount}" for category, amount in budgets.items()])
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """You are a financial advisor providing savings recommendations.
                Based on the user's spending history and budget, provide 3-5 practical, specific tips to help them save money.
                Format your response as a JSON array of strings, each string being one recommendation.
                Focus on actionable advice that can be implemented right away."""},
                {"role": "user", "content": f"""
                Total spending by category:
                {expense_summary}
                
                Budget by category:
                {budget_summary}
                """}
            ],
            response_format={"type": "json_object"}
        )
        recommendations = json.loads(response.choices[0].message.content)
        return recommendations.get("recommendations", [])
    except Exception as e:
        print(f"Error getting saving recommendations: {e}")
        return ["Unable to generate saving recommendations at this time."]

def get_budget_recommendations(expenses):
    """
    Generate budget recommendations based on spending history.
    """
    if not expenses or len(expenses) < 5:
        return {}
    
    # Calculate total expenses by category
    expenses_by_category = {}
    for expense in expenses:
        category = expense['category']
        amount = float(expense['amount'])
        if category in expenses_by_category:
            expenses_by_category[category] += amount
        else:
            expenses_by_category[category] = amount
    
    expense_summary = "\n".join([f"- {category}: ${amount:.2f}" for category, amount in expenses_by_category.items()])
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """You are a financial advisor providing budget recommendations.
                Based on the user's spending history, suggest monthly budget amounts for each category.
                Format your response as a JSON object with category names as keys and recommended monthly budget amounts as numeric values.
                Use the 50/30/20 rule or other appropriate budgeting principles."""},
                {"role": "user", "content": f"""
                Total spending by category:
                {expense_summary}
                
                Suggest a monthly budget for each category.
                """}
            ],
            response_format={"type": "json_object"}
        )
        budget_recommendations = json.loads(response.choices[0].message.content)
        return budget_recommendations
    except Exception as e:
        print(f"Error getting budget recommendations: {e}")
        return {}
