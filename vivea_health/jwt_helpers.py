# vivea_health/jwt_helpers.py
import jwt
from flask import request, jsonify
from functools import wraps

# Use an environment variable or configuration for security in production
SECRET_KEY = 'your-secret-key'

def verify_token():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            # Expect header format: "Bearer <token>"
            token = auth_header.split(" ")[1]
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return decoded  # Contains user info if needed
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = verify_token()
        if not user:
            return jsonify({'message': 'Token is missing or invalid!'}), 401
        return f(*args, **kwargs)
    return decorated
