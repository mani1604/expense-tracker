from flask import Flask, request, url_for, redirect, jsonify, render_template

app = Flask(__name__)

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
    return res

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
    return "<h1>My Dashboard</h1>"

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
