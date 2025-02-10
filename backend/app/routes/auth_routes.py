from flask import Blueprint, request, jsonify
from ..services.firebase_service import FirebaseService
from ..services.auth_service import AuthService
from ..models.user import User

auth_bp = Blueprint('auth', __name__)
firebase_service = FirebaseService()
auth_service = AuthService()

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
    token = auth_service.generate_token(user)
    
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
    
    token = auth_service.generate_token(user)
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
    })
