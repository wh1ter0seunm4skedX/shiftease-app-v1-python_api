import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
from .firebase_service import FirebaseService

class AuthService:
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.secret_key = os.getenv('JWT_SECRET')

    def generate_token(self, user):
        payload = {
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'exp': datetime.utcnow() + timedelta(days=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

def get_current_user():
    """Get the current user from the token in the request header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(" ")[1]
        auth_service = AuthService()
        payload = auth_service.verify_token(token)
        if payload:
            return {
                'user_id': payload['user_id'],
                'email': payload['email'],
                'role': payload['role']
            }
    except (IndexError, jwt.InvalidTokenError):
        return None
    
    return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = get_current_user()
        if not current_user:
            return jsonify({'message': 'Invalid or missing token'}), 401
        
        g.current_user = current_user
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = get_current_user()
        if not current_user:
            return jsonify({'message': 'Invalid or missing token'}), 401
        
        if current_user['role'] != 'manager':
            return jsonify({'message': 'Admin privileges required'}), 403
        
        g.current_user = current_user
        return f(*args, **kwargs)
    return decorated
