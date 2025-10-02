from flask import Flask, render_template, request, redirect, url_for
from model import db, Expense, Budget
from config import Config
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# --------------- Routes --------------- #

@app.route("/")
def home():
    return render_template("index.html")

# ✅ Add Expense
@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        amount = float(request.form["amount"])
        category = request.form.get("category", "Other")
        date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()

        new_expense = Expense(amount=amount, category=category, date=date)
        db.session.add(new_expense)
        db.session.commit()
        
        # Redirect to the budget page of the expense's month
        return redirect(url_for("check_budget", month=date.strftime("%b-%Y")))

    expenses = Expense.query.all()
    expenses_by_month = defaultdict(float)
    for e in expenses:
        month_name = e.date.strftime("%b-%Y")
        expenses_by_month[month_name] += e.amount

    return render_template("add_expense.html", expenses_by_month=expenses_by_month)



# ✅ Set Budget
@app.route("/set_budget", methods=["GET", "POST"])
def set_budget():
    if request.method == "POST":
        month = request.form["month"]  # e.g., "2025-11"
        limit = float(request.form.get("limit", 0))

        # Update if exists, else create new
        budget = Budget.query.filter_by(month=month).first()
        if budget:
            budget.goal_amount = limit
        else:
            budget = Budget(month=month, goal_amount=limit)
            db.session.add(budget)

        db.session.commit()
        return redirect(url_for("check_budget", month=month))  # <-- redirect dynamically

    return render_template("set_budget.html")


@app.route("/check_budget/<month>")
def check_budget(month):
    budget = Budget.query.filter_by(month=month).first()

    try:
        dt = datetime.strptime(month, "%b-%Y")
        month_number = dt.month
        year_number = dt.year
    except ValueError:
        month_number = None
        year_number = None

    expenses = Expense.query.all()
    spent = sum(
        e.amount for e in expenses
        if month_number and year_number and e.date.month == month_number and e.date.year == year_number
    )

    remaining = budget.goal_amount - spent if budget else 0

    if budget:
        if spent > budget.goal_amount:
            status = "Oh no! You exceeded your budget! 😢"
            img = "uncomfortable.png"
        else:
            status = "Great job! You're within budget! 😄"
            img = "happy.png"
    else:
        status = "No budget set for this month. 😢"
        img = "happy.png"

    return render_template(
        "check_budget.html",
                month=month,
        budget=budget.goal_amount if budget else 0,
        spent=spent,
        remaining=remaining,
        status=status,
        img=img
    )

    

if __name__ == "__main__":
    app.run( debug=True)
