from werkzeug.security import generate_password_hash, check_password_hash

passwd = "hi"
hash = generate_password_hash(passwd)
print(hash)
print(len(hash))

print(check_password_hash(hash, "hi9"))

import sqlite3

conn = sqlite3.connect("instance/expense.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables:")
for table in tables:
    print(table[0])