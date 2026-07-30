from flask import Flask, request, url_for, redirect, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Welcome to Expense Tracker</h1>"

@app.route("/expenses")
def expenses():
    res = f"""
<h1>My Expenses</h1>
<h2>Home URL: {url_for('home')}</h2>
<h2>Expenses URL: {url_for('expenses')}</h2>
<h2>Add URL: {url_for('add_expenses')}</h2>
"""
    return res

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

@app.route("/ping")
def ping():
    return "I am pinging"


@app.route('/api/summary')
def expense_summary():
    return jsonify({"total": 5100, 'currency': 'INR'})

if __name__ == "__main__":
    app.run(debug=True)
