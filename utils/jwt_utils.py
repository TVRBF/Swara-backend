import jwt
from datetime import datetime, timedelta
from config import Config

# Generate JWT token
def generate_token(user_id, role):
    payload = {
        "user_id": str(user_id),
        "role": role,
        "exp": datetime.utcnow() + timedelta(days=1)  # Token valid for 1 day
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

# Decode JWT token
def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
