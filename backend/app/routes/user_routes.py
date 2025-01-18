from flask import Blueprint, request, jsonify
from ..services.firebase_service import FirebaseService
from ..services.auth_service import admin_required

users_bp = Blueprint('users', __name__)
firebase_service = FirebaseService()

@users_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    users = firebase_service.get_all_users()
    return jsonify([{
        'id': user.id,
        **user.to_dict()
    } for user in users])

@users_bp.route('/<user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    user = firebase_service.get_user(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        **user.to_dict()
    })

@users_bp.route('/<user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    data = request.json
    user = firebase_service.get_user(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    firebase_service.update_user(user_id, data)
    return jsonify({'message': 'User updated successfully'})

@users_bp.route('/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = firebase_service.get_user(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    firebase_service.delete_user(user_id)
    return jsonify({'message': 'User deleted successfully'})
