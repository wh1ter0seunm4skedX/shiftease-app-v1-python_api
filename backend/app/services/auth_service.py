import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
from .firebase_service import FirebaseService

class AuthService:
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.secret_key = os.getenv('JWT_SECRET', 'your-secret-key-here')

    def generate_token(self, user_id: str) -> str:
        """
        Generate a JWT token for a user
        :param user_id: The user's ID
        :return: JWT token string
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token: str) -> str:
        """
        Verify a JWT token and return the user_id
        :param token: JWT token string
        :return: user_id if valid, raises exception if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            raise Exception('Token has expired')
        except jwt.InvalidTokenError:
            raise Exception('Invalid token')

def get_current_user():
    """Get the current user from the token in the request header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(" ")[1]
        auth_service = AuthService()
        user_id = auth_service.verify_token(token)
        current_user = auth_service.firebase_service.get_user(user_id)
        if current_user:
            return {
                'user_id': user_id,
                'email': current_user.email,
                'role': current_user.role
            }
    except (IndexError, jwt.InvalidTokenError):
        return None
    
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
        
        try:
            auth_service = AuthService()
            user_id = auth_service.verify_token(token)
            current_user = auth_service.firebase_service.get_user(user_id)
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
            g.current_user = current_user
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': str(e)}), 401
    
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
        
        try:
            auth_service = AuthService()
            user_id = auth_service.verify_token(token)
            current_user = auth_service.firebase_service.get_user(user_id)
            
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
                
            if current_user.role != 'admin':
                return jsonify({'message': 'Admin privileges required'}), 403
                
            g.current_user = current_user
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': str(e)}), 401
    
    return decorated
