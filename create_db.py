from app import app, db

# Creates the DB and creates the tables defined in models.py
with app.app_context():
    db.create_all()
