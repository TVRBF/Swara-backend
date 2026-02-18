import jwt
from datetime import datetime, timedelta
from config import Config

# Generate JWT token
def generate_token(user_id, role):
    if not Config.SECRET_KEY:
        raise Exception("SECRET_KEY is not set")

    payload = {
        "user_id": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

    # In case jwt returns bytes (older versions)
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token


# Decode JWT token
def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
