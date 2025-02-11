import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
from .firebase_service import FirebaseService

class AuthService:
    def __init__(self):
        self.firebase_service = FirebaseService()

def get_current_user():
    """Get the current user from the Firebase token in the request header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    
    try:
        token = auth_header.split(" ")[1]
        firebase_service = FirebaseService()
        decoded_token = firebase_service.verify_token(token)
        if decoded_token:
            return firebase_service.get_user_by_id(decoded_token['uid'])
        return None
    except Exception as e:
        print(f"Error getting current user: {str(e)}")
        return None

def token_required(f):
    """Decorator to verify Firebase token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'No token provided'}), 401

        try:
            token = auth_header.split(" ")[1]
            firebase_service = FirebaseService()
            decoded_token = firebase_service.verify_token(token)
            if not decoded_token:
                return jsonify({'message': 'Invalid token'}), 401
            
            # Store user info in Flask's g object
            g.user = firebase_service.get_user_by_id(decoded_token['uid'])
            if not g.user:
                return jsonify({'message': 'User not found'}), 401
                
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return jsonify({'message': 'Invalid token'}), 401

    return decorated

def admin_required(f):
    """Decorator to verify Firebase token and check if user is admin"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'No token provided'}), 401

        try:
            token = auth_header.split(" ")[1]
            firebase_service = FirebaseService()
            decoded_token = firebase_service.verify_token(token)
            if not decoded_token:
                return jsonify({'message': 'Invalid token'}), 401
            
            # Get user and check role
            user = firebase_service.get_user_by_id(decoded_token['uid'])
            if not user:
                return jsonify({'message': 'User not found'}), 401
            
            if user.role != 'admin':
                return jsonify({'message': 'Admin access required'}), 403
                
            # Store user info in Flask's g object
            g.user = user
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return jsonify({'message': 'Invalid token'}), 401

    return decorated
