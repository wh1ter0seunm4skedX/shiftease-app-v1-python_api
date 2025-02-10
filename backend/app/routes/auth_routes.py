from flask import Blueprint, request, jsonify
from ..services.firebase_service import FirebaseService, firebase_token_required
from ..models.user import User

auth_bp = Blueprint('auth', __name__)
firebase_service = FirebaseService()

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
    token = firebase_service.generate_token(user_id)
    
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
    token = firebase_service.generate_token(user.id)
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'role': user.role
        }
    }), 200

@auth_bp.route('/test-auth', methods=['GET'])
@firebase_token_required
def test_auth():
    """Test endpoint to verify Firebase authentication is working"""
    try:
        firebase_user = request.firebase_user
        return jsonify({
            'message': 'Authentication successful',
            'user': {
                'uid': firebase_user['uid'],
                'email': firebase_user['email'],
                'firebase_verified': True
            }
        }), 200
    except Exception as e:
        return jsonify({'message': f'Authentication error: {str(e)}'}), 500

@auth_bp.route('/me', methods=['GET'])
@firebase_token_required
def get_current_user():
    """Get the current user's profile"""
    try:
        # Get the Firebase user from the request context
        firebase_user = request.firebase_user
        
        # Get the user from Firestore
        user = firebase_service.get_user_by_id(firebase_user['uid'])
        if not user:
            return jsonify({'message': 'User not found'}), 404
            
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/create-profile', methods=['POST'])
@firebase_token_required
def create_profile():
    """Create a new user profile after Firebase authentication"""
    try:
        data = request.get_json()
        firebase_user = request.firebase_user
        
        # Create user in Firestore
        user = User(
            id=firebase_user['uid'],
            email=firebase_user['email'],
            name=data.get('name', ''),
            role=data.get('role', 'worker')
        )
        
        # Save user to Firestore
        firebase_service.create_user(user)
        
        # Set custom claims
        firebase_service.set_custom_claims(firebase_user['uid'], {'role': user.role})
        
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/update-profile', methods=['PUT'])
@firebase_token_required
def update_profile():
    """Update the current user's profile"""
    try:
        data = request.get_json()
        firebase_user = request.firebase_user
        
        # Get existing user
        user = firebase_service.get_user_by_id(firebase_user['uid'])
        if not user:
            return jsonify({'message': 'User not found'}), 404
            
        # Update user fields
        if 'name' in data:
            user.name = data['name']
        if 'role' in data:
            user.role = data['role']
            # Update custom claims if role changes
            firebase_service.set_custom_claims(firebase_user['uid'], {'role': user.role})
            
        # Save updated user
        firebase_service.update_user(user)
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@firebase_token_required
def refresh_token():
    # Generate new token
    firebase_user = request.firebase_user
    new_token = firebase_service.generate_token(firebase_user['uid'])
    return jsonify({
        'token': new_token,
        'user': {
            'id': firebase_user['uid'],
            'email': firebase_user['email'],
            'name': firebase_user['name'],
            'role': firebase_user['role']
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@firebase_token_required
def logout():
    # In a more complex implementation, you might want to invalidate the token here
    return jsonify({'message': 'Successfully logged out'}), 200
