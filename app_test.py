from werkzeug.security import generate_password_hash, check_password_hash

passwd = "hi"
hash = generate_password_hash(passwd)
print(hash)
print(len(hash))

print(check_password_hash(hash, "hi9"))

from app import User

user = User.query.filter_by(username="tom123").first()
print(user)
