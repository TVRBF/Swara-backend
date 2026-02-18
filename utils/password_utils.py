import bcrypt

# Hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

# Verify a password
def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
