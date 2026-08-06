from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from app import db, User, Expense

load_dotenv()

# SQLite
sqlite_db = os.path.abspath("instance/expense.db")
sqlite_engine = create_engine(f"sqlite:///{sqlite_db}")

# PostgreSQL
dest_db = os.environ["POSTGRES_RENDER_URL"]
postgres_engine = create_engine(dest_db)

# Create tables in PostgreSQL
db.metadata.create_all(bind=postgres_engine)

SQLiteSession = sessionmaker(bind=sqlite_engine)
PostgresSession = sessionmaker(bind=postgres_engine)

sqlite = SQLiteSession()
postgres = PostgresSession()

# Copy Users
for user in sqlite.query(User).all():
    postgres.add(
        User(
            id=user.id,
            username=user.username,
            email=user.email,
            password=user.password,
        )
    )

postgres.commit()

# Copy Expenses
for expense in sqlite.query(Expense).all():
    postgres.add(
        Expense(
            id=expense.id,
            description=expense.description,
            amount=expense.amount,
            category=expense.category,
            date=expense.date,
            user_id=expense.user_id,
        )
    )

postgres.commit()

print("Migration completed!")
