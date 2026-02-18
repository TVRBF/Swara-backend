import bcrypt

# Hash a password (store as string safely in MongoDB)
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")  # store as string


# Verify a password
def verify_password(password, hashed):
    if not hashed:
        return False

    # If hashed comes from MongoDB as string, convert to bytes
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")

    return bcrypt.checkpw(password.encode("utf-8"), hashed)
