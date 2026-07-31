from flask import Flask, request, url_for, redirect, jsonify, render_template

app = Flask(__name__)

# Hardcoded data, we will replace it with DB later
user_expenses = [
        {'id': 1, 'description': 'Groceries', 'amount': 850, 'category': 'Food', 'date': '20-01-2026'},
        {'id': 2, 'description': 'Uber ride', 'amount': 220.9765, 'category': 'Transport', 'date': '10-02-2026'},
        {'id': 3, 'description': 'Lunch', 'amount': 400, 'category': 'Food', 'date': '04-03-2026'},
        {'id': 4, 'description': 'Electricity bill', 'amount': 1200, 'category': 'Bills', 'date': '14-03-2026'},
        {'id': 5, 'description': 'Ola ride', 'amount': 180, 'category': 'Transport', 'date': '27-04-2026'},
        {'id': 6, 'description': 'Netflix', 'amount': 499, 'category': 'Entertainment', 'date': '11-05-2026'},
    ]

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
    if request.method == "GET":
        return "<form method='POST'><input name='desc'><button>Add</button></form>"
    elif request.method == "POST":
        desc = request.form.get('desc')
        print(f"Added {desc}")
        return redirect(url_for('add_expenses'))

@app.route('/dashboard')
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

@app.route('/register')
def register():
    return "<h1>Register</h1>"

@app.route('/login')
def login():
    return "<h1>Login</h1>"

@app.route('/logout')
def logout():
    return "<h1>Logout</h1>"

@app.route("/ping")
def ping():
    return "I am pinging"


@app.route('/api/summary')
def expense_summary():
    return jsonify({"total": 5100, 'currency': 'INR'})

if __name__ == "__main__":
    app.run(debug=True)
