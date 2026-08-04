from flask import Flask, request, url_for, redirect, jsonify, render_template, flash
from dotenv import load_dotenv
import os
from functools import wraps
from forms import ExpenseForm, RegisterForm, LoginForm
from flask import session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv() # reads the .env file & loads the env variables

app = Flask(__name__)

"""
How to generate secret key:
1. Open terminal

2. Run the below command:
python -c "import secrets; print(secrets.token_hex(32))"

3. Copy the output of this command and paste it in .env file

NOTE: secret key is required for Flask-WForms and Flash messages
"""
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")

# DB config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
# Hardcoded data, we will replace it with DB later
users = []

user_expenses = [
        {'id': 1, 'description': 'Groceries', 'amount': 850, 'category': 'Food', 'date': '20-01-2026'},
        {'id': 2, 'description': 'Uber ride', 'amount': 220.9765, 'category': 'Transport', 'date': '10-02-2026'},
        {'id': 3, 'description': 'Lunch', 'amount': 400, 'category': 'Food', 'date': '04-03-2026'},
        {'id': 4, 'description': 'Electricity bill', 'amount': 1200, 'category': 'Bills', 'date': '14-03-2026'},
        {'id': 5, 'description': 'Ola ride', 'amount': 180, 'category': 'Transport', 'date': '27-04-2026'},
        {'id': 6, 'description': 'Netflix', 'amount': 499, 'category': 'Entertainment', 'date': '11-05-2026'},
    ]

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
def expenses():
    res = f"""
<h1>My Expenses</h1>
<h2>Home URL: {url_for('home')}</h2>
<h2>Expenses URL: {url_for('expenses')}</h2>
<h2>Add URL: {url_for('add_expenses')}</h2>
"""
    return render_template("expenses.html", expenses=user_expenses)

@app.route('/expenses/<int:expense_id>')
def expense_detail(expense_id):
    return f"<h1>Expense ID: {expense_id}</h1>"

@app.route('/expenses/<int:expense_id>/delete', methods=["POST"])
def delete_expense(expense_id):
    # The expense gets deleted from the DB
    return redirect(url_for('expenses'))

@app.route('/expenses/category/<string:category_name>')
def expenses_by_category(category_name):
    return f"<h2>Expenses in category {category_name}</h2>"

@app.route("/add", methods=["GET", "POST"])
def add_expenses():
    form = ExpenseForm()

    if form.validate_on_submit():
        description = form.description.data
        amount = form.amount.data
        category = form.category.data

        # Save the data in DB (later)
        flash(f"Expense of amount {amount} added.", "success")
        return redirect(url_for('expenses'))

    return render_template('add_expense.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    total = 0
    categories = set()
    for expense in user_expenses:
        total += expense['amount']
        categories.add(expense['category'])

    n_categories = len(categories)
    n_transactions = len(user_expenses)

    # Calculating the category wise total amount
    breakdown_amount = {}
    for expense in user_expenses:
        if expense['category'] in breakdown_amount:
             breakdown_amount[expense['category']] += expense['amount']
        else:
            breakdown_amount[expense['category']] = expense['amount']
    
    return render_template("dashboard.html", username="John", total_amount=total, 
                           count=n_transactions,categories=n_categories,
                           breakdown=breakdown_amount)

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # check user exists
        for user in users:
            if user['username'] == form.username.data:
                flash("Username already exists, choose a different username", "error")
                return render_template("register.html", form=form)
            elif user['email'] == form.email.data:
                flash("Account already exists with the email", "error")
                return render_template("register.html", form=form)
        users.append({
            'id': len(users) + 1,
            'username': form.username.data,
            'email': form.email.data,
            'password': generate_password_hash(form.password.data)
        })
        flash("Account created! Please login", "success")
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = None
        for u in users:
            if u['email'] == form.email.data:
                user = u
                break

        if user and check_password_hash(u['password'], form.password.data):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f"Welcome back, {user['username']}", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "error")
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been sucessfully logged out!", "success")
    return redirect(url_for("home"))

@app.route("/ping")
def ping():
    return f'Users:{users}'

@app.route('/api/summary')
def expense_summary():
    return jsonify({"total": 5100, 'currency': 'INR'})

if __name__ == "__main__":
    app.run(debug=True)
