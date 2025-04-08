import os
import json
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Text, JSON, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to connect to PostgreSQL, fall back to SQLite if it fails
try:
    # First, try to use the direct DATABASE_URL environment variable (most likely to work)
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL:
        logger.info(f"Attempting to connect using DATABASE_URL: {DATABASE_URL}")
    
        # Clean up DATABASE_URL if it uses newer format with postgresql+psycopg://
        clean_url = DATABASE_URL
        if clean_url.startswith("postgresql+psycopg://"):
            clean_url = clean_url.replace("postgresql+psycopg://", "postgresql://")
            
        # Create engine with connection timeout and detailed logging
        engine = create_engine(
            clean_url, 
            connect_args={"connect_timeout": 10},
            echo=True  # This will log all SQL queries
        )
        
        # Test the connection
        with engine.connect() as conn:
            # Run a simple query to verify the connection
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            
        logger.info("Successfully connected to PostgreSQL database via DATABASE_URL")
        
    # If DATABASE_URL not available, try to build it from individual environment variables
    else:
        # Check for individual PostgreSQL connection variables
        pg_user = os.environ.get("PGUSER")
        pg_password = os.environ.get("PGPASSWORD")
        pg_host = os.environ.get("PGHOST")
        pg_port = os.environ.get("PGPORT")
        pg_database = os.environ.get("PGDATABASE")
        
        # Log the values for troubleshooting
        logger.info(f"PGUSER: {pg_user}")
        logger.info(f"PGHOST: {pg_host}")
        logger.info(f"PGPORT: {pg_port}")
        logger.info(f"PGDATABASE: {pg_database}")
        # We don't log the password for security reasons
        
        # Construct a new connection URL if all required parts exist
        if pg_user and pg_password and pg_host and pg_port and pg_database:
            # Build PostgreSQL connection URL from parts
            postgres_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}?sslmode=require"
            logger.info(f"Attempting to connect using constructed URL to {pg_host}")
            
            # Create engine with connection timeout and detailed logging
            engine = create_engine(
                postgres_url,
                connect_args={"connect_timeout": 10},
                echo=True  # This will log all SQL queries
            )
            
            # Test the connection
            with engine.connect() as conn:
                # Run a simple query to verify the connection
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
                
            logger.info("Successfully connected to PostgreSQL database via constructed URL")
        else:
            raise ValueError("PostgreSQL connection information not available")
except Exception as e:
    logger.warning(f"Failed to connect to PostgreSQL: {e}")
    logger.info("Falling back to SQLite database")
    # Create SQLite engine with foreign key support
    engine = create_engine("sqlite:///finance_assistant.db", connect_args={"check_same_thread": False})

Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define models
class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    category = Column(String(50), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "amount": str(self.amount),
            "date": self.date.strftime("%Y-%m-%d"),
            "category": self.category
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            description=data["description"],
            amount=float(data["amount"]),
            date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
            category=data["category"]
        )

class Budget(Base):
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True)
    category = Column(String(50), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "amount": str(self.amount)
        }

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, nullable=False, default=0)
    target_date = Column(Date, nullable=False)
    priority = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)
    created_date = Column(Date, nullable=False, default=datetime.now().date())
    progress_updates = Column(JSON, nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "target_amount": str(self.target_amount),
            "current_amount": str(self.current_amount),
            "target_date": self.target_date.strftime("%Y-%m-%d"),
            "priority": self.priority,
            "notes": self.notes or "",
            "created_date": self.created_date.strftime("%Y-%m-%d"),
            "progress_updates": self.progress_updates or []
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            target_amount=float(data["target_amount"]),
            current_amount=float(data["current_amount"]),
            target_date=datetime.strptime(data["target_date"], "%Y-%m-%d").date(),
            priority=data["priority"],
            notes=data["notes"],
            created_date=datetime.strptime(data["created_date"], "%Y-%m-%d").date() if "created_date" in data else datetime.now().date(),
            progress_updates=data.get("progress_updates", [])
        )

class Insight(Base):
    __tablename__ = "insights"
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_date = Column(Date, nullable=False, default=datetime.now().date())
    
    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "created_date": self.created_date.strftime("%Y-%m-%d")
        }

# Database operations
def init_db():
    """Initialize the database tables."""
    Base.metadata.create_all(engine)

def get_all_expenses():
    """Get all expenses from the database."""
    session = Session()
    try:
        expenses = session.query(Expense).all()
        return [expense.to_dict() for expense in expenses]
    finally:
        session.close()

def add_expense(expense_data):
    """Add a new expense to the database."""
    session = Session()
    try:
        expense = Expense.from_dict(expense_data)
        session.add(expense)
        session.commit()
        return expense.to_dict()
    finally:
        session.close()

def delete_expense(expense_id):
    """Delete an expense from the database."""
    session = Session()
    try:
        expense = session.query(Expense).filter(Expense.id == expense_id).first()
        if expense:
            session.delete(expense)
            session.commit()
            return True
        return False
    finally:
        session.close()

def get_all_budgets():
    """Get all budgets from the database."""
    session = Session()
    try:
        budgets = session.query(Budget).all()
        return {budget.category: str(budget.amount) for budget in budgets}
    finally:
        session.close()

def save_budget(category, amount):
    """Save or update a budget."""
    session = Session()
    try:
        budget = session.query(Budget).filter(Budget.category == category).first()
        if budget:
            budget.amount = amount
        else:
            budget = Budget(category=category, amount=amount)
            session.add(budget)
        session.commit()
        return True
    finally:
        session.close()

def save_budgets(budgets_dict):
    """Save multiple budgets at once."""
    session = Session()
    try:
        # Clear existing budgets
        session.query(Budget).delete()
        
        # Add new budgets
        for category, amount in budgets_dict.items():
            budget = Budget(category=category, amount=float(amount))
            session.add(budget)
        
        session.commit()
        return True
    finally:
        session.close()

def get_all_goals():
    """Get all financial goals from the database."""
    session = Session()
    try:
        goals = session.query(Goal).all()
        return [goal.to_dict() for goal in goals]
    finally:
        session.close()

def add_goal(goal_data):
    """Add a new financial goal to the database."""
    session = Session()
    try:
        goal = Goal.from_dict(goal_data)
        session.add(goal)
        session.commit()
        return goal.to_dict()
    finally:
        session.close()

def update_goal(goal_id, goal_data):
    """Update an existing financial goal."""
    session = Session()
    try:
        goal = session.query(Goal).filter(Goal.id == goal_id).first()
        if goal:
            goal.name = goal_data.get("name", goal.name)
            goal.target_amount = float(goal_data.get("target_amount", goal.target_amount))
            goal.current_amount = float(goal_data.get("current_amount", goal.current_amount))
            goal.target_date = datetime.strptime(goal_data.get("target_date", goal.target_date.strftime("%Y-%m-%d")), "%Y-%m-%d").date()
            goal.priority = goal_data.get("priority", goal.priority)
            goal.notes = goal_data.get("notes", goal.notes)
            goal.progress_updates = goal_data.get("progress_updates", goal.progress_updates)
            session.commit()
            return goal.to_dict()
        return None
    finally:
        session.close()

def delete_goal(goal_id):
    """Delete a financial goal."""
    session = Session()
    try:
        goal = session.query(Goal).filter(Goal.id == goal_id).first()
        if goal:
            session.delete(goal)
            session.commit()
            return True
        return False
    finally:
        session.close()

def save_insights(insights):
    """Save financial insights to the database."""
    session = Session()
    try:
        # Clear old insights
        session.query(Insight).delete()
        
        # Add new insights
        for insight in insights:
            new_insight = Insight(content=insight)
            session.add(new_insight)
        
        session.commit()
        return True
    finally:
        session.close()

def get_insights():
    """Get all financial insights from the database."""
    session = Session()
    try:
        insights = session.query(Insight).all()
        return [insight.content for insight in insights]
    finally:
        session.close()

# Import/export functions
def export_data():
    """Export all data to a dictionary."""
    return {
        "expenses": get_all_expenses(),
        "budgets": get_all_budgets(),
        "goals": get_all_goals(),
        "insights": get_insights()
    }

def import_data(data):
    """Import data from a dictionary."""
    session = Session()
    try:
        # Clear existing data
        session.query(Expense).delete()
        session.query(Budget).delete()
        session.query(Goal).delete()
        session.query(Insight).delete()
        
        # Import expenses
        for expense_data in data.get("expenses", []):
            session.add(Expense.from_dict(expense_data))
        
        # Import budgets
        for category, amount in data.get("budgets", {}).items():
            session.add(Budget(category=category, amount=float(amount)))
        
        # Import goals
        for goal_data in data.get("goals", []):
            session.add(Goal.from_dict(goal_data))
        
        # Import insights
        for insight in data.get("insights", []):
            session.add(Insight(content=insight))
        
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()