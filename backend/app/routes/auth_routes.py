from flask import Blueprint, request, jsonify
from functools import wraps
from ..services.firebase_service import FirebaseService
from ..services.auth_service import AuthService
from ..models.user import User

auth_bp = Blueprint('auth', __name__)
firebase_service = FirebaseService()
auth_service = AuthService()

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
            user_id = auth_service.verify_token(token)
            current_user = firebase_service.get_user(user_id)
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
            return f(current_user, *args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Invalid token'}), 401
    
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not all(k in data for k in ['email', 'password', 'name', 'role']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    if firebase_service.get_user_by_email(data['email']):
        return jsonify({'message': 'User already exists'}), 400
    
    # Create new user
    user = User(
        email=data['email'],
        name=data['name'],
        role=data['role'],
        password=data['password']  # In production, this should be hashed
    )
    
    user_id = firebase_service.create_user(user)
    
    # Generate token for the new user
    token = auth_service.generate_token(user_id)
    
    return jsonify({
        'message': 'User created successfully',
        'token': token,
        'user': {
            'id': user_id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    user = firebase_service.get_user_by_email(data['email'])
    if not user or user.password != data['password']:  # In production, properly compare hashed passwords
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Generate token
    token = auth_service.generate_token(user.id)
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    return jsonify({
        'id': current_user.id,
        'email': current_user.email,
        'name': current_user.name,
        'role': current_user.role
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@token_required
def refresh_token(current_user):
    # Generate new token
    new_token = auth_service.generate_token(current_user.id)
    return jsonify({
        'token': new_token,
        'user': {
            'id': current_user.id,
            'email': current_user.email,
            'name': current_user.name,
            'role': current_user.role
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    # In a more complex implementation, you might want to invalidate the token here
    return jsonify({'message': 'Successfully logged out'}), 200
