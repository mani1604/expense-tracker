from flask import Flask, request, url_for, redirect, jsonify, render_template, flash
from dotenv import load_dotenv
import os
from datetime import datetime
from functools import wraps
from forms import ExpenseForm, RegisterForm, LoginForm
from flask import session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv() # reads the .env file & loads the env variables

app = Flask(__name__)

"""
How to generate secret key:
1. Open terminal

2. Run the below command:
python -c "import secrets; print(secrets.token_hex(32))"

3. Copy the output of this command and paste it in .env file

NOTE: secret key is required for Flask-WTForms and Flash messages
"""
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("POSTGRES_RENDER_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from pathlib import Path

with app.app_context():
    print("URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("Engine URL:", db.engine.url)
    print("Database file:", Path(db.engine.url.database).resolve())

migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    expenses = db.relationship("Expense", backref='owner', lazy=True)

    def _str__(self):
        return f"{self.username}"

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def _str__(self):
            return f"Expense {self.description} for {self.amount}"

# Hardcoded data, we will replace it with DB later
# users = []

# user_expenses = [
#         {'id': 1, 'description': 'Groceries', 'amount': 850, 'category': 'Food', 'date': '20-01-2026'},
#         {'id': 2, 'description': 'Uber ride', 'amount': 220.9765, 'category': 'Transport', 'date': '10-02-2026'},
#         {'id': 3, 'description': 'Lunch', 'amount': 400, 'category': 'Food', 'date': '04-03-2026'},
#         {'id': 4, 'description': 'Electricity bill', 'amount': 1200, 'category': 'Bills', 'date': '14-03-2026'},
#         {'id': 5, 'description': 'Ola ride', 'amount': 180, 'category': 'Transport', 'date': '27-04-2026'},
#         {'id': 6, 'description': 'Netflix', 'amount': 499, 'category': 'Entertainment', 'date': '11-05-2026'},
#     ]

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to continue.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/expenses")
@login_required
def expenses():
    res = f"""
<h1>My Expenses</h1>
<h2>Home URL: {url_for('home')}</h2>
<h2>Expenses URL: {url_for('expenses')}</h2>
<h2>Add URL: {url_for('add_expenses')}</h2>
"""
    user_expenses = Expense.query.filter_by(user_id=session["user_id"]).order_by(Expense.date.desc()).all()
    return render_template("expenses.html", expenses=user_expenses)

# TODO:  Fetch data from DB
@app.route('/expenses/<int:expense_id>')
@login_required
def expense_detail(expense_id):
    return f"<h1>Expense ID: {expense_id}</h1>"

@app.route('/expenses/<int:expense_id>/delete', methods=["POST"])
@login_required
def delete_expense(expense_id):
    # The expense gets deleted from the DB
    expense = Expense.query.filter_by(id=expense_id, user_id=session['user_id']).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('expenses'))

@app.route('/expenses/category/<string:category_name>')
@login_required
def expenses_by_category(category_name):
    return f"<h2>Expenses in category {category_name}</h2>"

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_expenses():
    form = ExpenseForm()

    if form.validate_on_submit():
        description = form.description.data
        amount = form.amount.data
        category = form.category.data

        expense = Expense(description=description, amount=amount, 
                          category=category, user_id=session["user_id"])

        db.session.add(expense) # adding expense to DB
        db.session.commit()
        flash(f"Expense of amount {amount} added.", "success")
        return redirect(url_for('expenses'))

    return render_template('add_expense.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    total = 0
    categories = set()
    current_user = session["user_id"]
    user_expenses = Expense.query.filter_by(user_id=current_user).all()
    for expense in user_expenses:
        total += expense.amount
        categories.add(expense.category)

    n_categories = len(categories)
    n_transactions = len(user_expenses)

    # Calculating the category wise total amount
    breakdown_amount = {}
    for expense in user_expenses:
        if expense.category in breakdown_amount:
             breakdown_amount[expense.category] += expense.amount
        else:
            breakdown_amount[expense.category] = expense.amount
    
    return render_template("dashboard.html", username=session["username"], total_amount=total, 
                           count=n_transactions,categories=n_categories,
                           breakdown=breakdown_amount)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # check user exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists, choose a different username", "error")
            return render_template("register.html", form=form)
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash("Account already exists with the email", "error")
            return render_template("register.html", form=form)

        # Add user to DB
        user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()

        flash("Account created! Please login", "success")
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user and check_password_hash(existing_user.password, form.password.data):
            session['user_id'] = existing_user.id
            session['username'] = existing_user.username
            flash(f"Welcome back, {existing_user.username}", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "error")
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("You have been sucessfully logged out!", "success")
    return redirect(url_for("home"))

@app.route("/users")
def get_users():
    all_users = User.query.all()
    result = ''
    for u in all_users:
        result += f"ID: {u.id}, Username: {u.username}, Email: {u.email}<br>"

    u =  User.query.filter_by(email="jerry@gmail.com").first()
    result += str(u.email)
    return result

@app.route("/ping")
def ping():
    return f'Hello {session["username"]}'

# Example of API route
@app.route('/api/summary')
def expense_summary():
    return jsonify({"total": 5100, 'currency': 'INR'})

if __name__ == "__main__":
    app.run(debug=True)
