import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
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

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        auth_service = AuthService()
        payload = auth_service.verify_token(token)
        
        if not payload:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        auth_service = AuthService()
        payload = auth_service.verify_token(token)
        
        if not payload:
            return jsonify({'message': 'Invalid token'}), 401

        if payload['role'] != 'manager':
            return jsonify({'message': 'Admin privileges required'}), 403

        return f(*args, **kwargs)
    return decorated
