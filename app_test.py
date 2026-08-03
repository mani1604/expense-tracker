from werkzeug.security import generate_password_hash, check_password_hash

passwd = "hi"
hash = generate_password_hash(passwd)
print(hash)

print(check_password_hash(hash, "hi9"))