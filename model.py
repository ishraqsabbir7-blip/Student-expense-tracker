from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), default="Other")
    date = db.Column(db.Date, nullable=False)

class Budget(db.Model):
    __tablename__ = "budget_goals"
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    goal_amount = db.Column(db.Float, nullable=False)
