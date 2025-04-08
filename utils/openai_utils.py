import os
import json
import logging
from openai import OpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Check if API key is available
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not found in environment variables. AI features will be limited.")
    client = None
else:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        logger.info("Successfully initialized OpenAI client")
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {e}")
        client = None

def categorize_expense(description, amount):
    """
    Use OpenAI to categorize an expense based on its description.
    """
    # Check if client is initialized
    if client is None:
        logger.warning("OpenAI client not available. Using default category.")
        return "Other"
    
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
        logger.error(f"Error categorizing expense: {e}")
        
        # Use simple keyword matching as fallback
        description_lower = description.lower()
        if any(word in description_lower for word in ["rent", "mortgage", "electric", "water", "gas bill", "internet"]):
            return "Housing"
        elif any(word in description_lower for word in ["car", "gas", "uber", "lyft", "taxi", "bus", "train", "subway"]):
            return "Transportation"
        elif any(word in description_lower for word in ["grocery", "restaurant", "food", "dinner", "lunch", "breakfast"]):
            return "Food"
        elif any(word in description_lower for word in ["movie", "game", "netflix", "spotify", "concert", "theater"]):
            return "Entertainment"
        elif any(word in description_lower for word in ["clothes", "shirt", "shoes", "dress", "electronics", "phone"]):
            return "Shopping"
        elif any(word in description_lower for word in ["doctor", "hospital", "medicine", "prescription", "therapy"]):
            return "Health"
        elif any(word in description_lower for word in ["tuition", "course", "book", "school", "college", "university"]):
            return "Education"
        elif any(word in description_lower for word in ["flight", "hotel", "vacation", "trip", "airbnb"]):
            return "Travel"
        elif any(word in description_lower for word in ["saving", "investment", "stock", "bond", "401k", "ira"]):
            return "Savings/Investment"
        else:
            return "Other"

def analyze_spending_patterns(expenses):
    """
    Analyze spending patterns and provide insights.
    """
    if not expenses or len(expenses) < 3:
        return ["Not enough expense data to analyze patterns. Add more expenses to get insights."]
    
    # Check if client is initialized
    if client is None:
        logger.warning("OpenAI client not available. Using basic insights.")
        # Return basic insights
        category_totals = {}
        for expense in expenses:
            category = expense['category']
            amount = float(expense['amount'])
            if category in category_totals:
                category_totals[category] += amount
            else:
                category_totals[category] = amount
        
        # Sort categories by amount (highest first)
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        insights = []
        if sorted_categories:
            insights.append(f"Your highest spending category is {sorted_categories[0][0]} at ${sorted_categories[0][1]:.2f}.")
        
        if len(sorted_categories) >= 2:
            insights.append(f"Consider reducing spending in your top categories: {sorted_categories[0][0]} and {sorted_categories[1][0]}.")
            
        insights.append("Track expenses consistently to get more detailed AI-powered insights.")
        return insights
        
    expenses_text = "\n".join([f"Category: {e['category']}, Amount: ${e['amount']}, Date: {e['date']}, Description: {e['description']}" for e in expenses])
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """You are a financial advisor analyzing spending patterns.
                Provide 3-5 concise, actionable insights about spending patterns.
                Format your response as a JSON object with an 'insights' key containing an array of strings, each string being one insight.
                Be specific, practical, and focus on areas where the user could save money."""},
                {"role": "user", "content": f"Here are the recent expenses:\n{expenses_text}"}
            ],
            response_format={"type": "json_object"}
        )
        insights_data = json.loads(response.choices[0].message.content)
        return insights_data.get("insights", ["Track expenses consistently to get more detailed AI-powered insights."])
    except Exception as e:
        logger.error(f"Error analyzing spending patterns: {e}")
        return ["Unable to analyze spending patterns at this time. Please try again later."]

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
    
    # Check if client is initialized
    if client is None:
        logger.warning("OpenAI client not available. Using basic recommendations.")
        
        # Generate basic recommendations
        recommendations = []
        
        # Check for over-budget categories
        for category, amount in expenses_by_category.items():
            budget_amount = float(budgets.get(category, 0))
            if budget_amount > 0 and amount > budget_amount:
                recommendations.append(f"You're over budget in {category}. Try to reduce spending in this category.")
        
        # Add general recommendations
        if "Food" in expenses_by_category:
            recommendations.append("Consider meal planning to reduce food expenses and minimize waste.")
            
        if "Entertainment" in expenses_by_category:
            recommendations.append("Look for free or low-cost entertainment options in your area.")
            
        if "Shopping" in expenses_by_category:
            recommendations.append("Consider implementing a 24-hour rule before making non-essential purchases.")
            
        if not recommendations:
            recommendations.append("Track more expenses to get personalized saving recommendations.")
            
        return recommendations[:5]  # Return up to 5 recommendations
    
    expense_summary = "\n".join([f"- {category}: ${amount:.2f}" for category, amount in expenses_by_category.items()])
    budget_summary = "\n".join([f"- {category}: ${amount}" for category, amount in budgets.items()])
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """You are a financial advisor providing savings recommendations.
                Based on the user's spending history and budget, provide 3-5 practical, specific tips to help them save money.
                Format your response as a JSON object with a 'recommendations' key containing an array of strings, each string being one recommendation.
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
        recommendations_data = json.loads(response.choices[0].message.content)
        return recommendations_data.get("recommendations", ["Track more expenses to get personalized saving recommendations."])
    except Exception as e:
        logger.error(f"Error getting saving recommendations: {e}")
        return ["Unable to generate saving recommendations at this time. Please try again later."]

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
            
    # Check if client is initialized
    if client is None:
        logger.warning("OpenAI client not available. Using simple budget recommendations.")
        
        # Calculate total spending
        total_spending = sum(expenses_by_category.values())
        
        # Apply a simple 50/30/20 rule:
        # 50% for needs, 30% for wants, 20% for savings
        budget_recommendations = {}
        
        # Categorize each expense category into needs, wants, or savings
        needs = ["Housing", "Transportation", "Food", "Health"]
        wants = ["Entertainment", "Shopping", "Travel"]
        savings = ["Savings/Investment"]
        
        # Calculate budget for each category
        for category, amount in expenses_by_category.items():
            if category in needs:
                # Allocate a bit more than current spending for needs
                budget_recommendations[category] = round(amount * 1.1, 2)
            elif category in wants:
                # Reduce spending on wants if necessary
                budget_recommendations[category] = round(amount * 0.9, 2)
            elif category in savings:
                # Increase savings
                budget_recommendations[category] = round(amount * 1.2, 2)
            else:
                # Keep other categories the same
                budget_recommendations[category] = round(amount, 2)
        
        # Make sure we have at least one entry for each major category type
        if not any(category in budget_recommendations for category in needs):
            budget_recommendations["Housing"] = round(total_spending * 0.3, 2)
            
        if not any(category in budget_recommendations for category in wants):
            budget_recommendations["Entertainment"] = round(total_spending * 0.1, 2)
            
        if not any(category in budget_recommendations for category in savings):
            budget_recommendations["Savings/Investment"] = round(total_spending * 0.2, 2)
            
        return budget_recommendations
    
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
        logger.error(f"Error getting budget recommendations: {e}")
        
        # Fallback to simple calculation
        basic_recommendations = {}
        for category, amount in expenses_by_category.items():
            basic_recommendations[category] = round(amount, 2)
            
        return basic_recommendations
