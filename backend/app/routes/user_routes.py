from flask import Blueprint, request, jsonify, g
from ..services.firebase_service import FirebaseService
from ..services.auth_service import token_required, admin_required
from datetime import datetime

users_bp = Blueprint('users', __name__)
firebase_service = FirebaseService()

@users_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    """Get the current user's profile"""
    return jsonify({
        'id': g.user.id,
        **g.user.to_dict()
    })

@users_bp.route('/me/events', methods=['GET'])
@token_required
def get_my_events():
    """Get all events the current user is registered for"""
    events = []
    for event_id in g.user.registered_events:
        event = firebase_service.get_event(event_id)
        if event:
            events.append({
                'id': event.id,
                **event.to_dict()
            })
    return jsonify(events)

@users_bp.route('/', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users (admin only)"""
    users = firebase_service.get_all_users()
    return jsonify([{
        'id': user.id,
        **user.to_dict()
    } for user in users])

@users_bp.route('/<user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """Get a specific user's profile (admin only)"""
    user = firebase_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        **user.to_dict()
    })

@users_bp.route('/me', methods=['PUT'])
@token_required
def update_my_profile():
    """Update current user's profile"""
    data = request.json
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    # Only allow updating certain fields
    allowed_fields = {'name'}
    update_data = {k: v for k, v in data.items() if k in allowed_fields}
    
    if not update_data:
        return jsonify({'message': 'No valid fields to update'}), 400
    
    success = firebase_service.update_user(g.user.id, update_data)
    if not success:
        return jsonify({'message': 'Failed to update profile'}), 500
    
    return jsonify({'message': 'Profile updated successfully'})

@users_bp.route('/<user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(user_id):
    """Update a user's role (admin only)"""
    data = request.json
    if not data or 'role' not in data:
        return jsonify({'message': 'Role is required'}), 400
    
    if data['role'] not in ['admin', 'worker']:
        return jsonify({'message': 'Invalid role'}), 400
    
    success = firebase_service.update_user(user_id, {'role': data['role']})
    if not success:
        return jsonify({'message': 'Failed to update user role'}), 500
    
    return jsonify({'message': 'User role updated successfully'})

@users_bp.route('/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user (admin only)"""
    # Don't allow deleting yourself
    if user_id == g.user.id:
        return jsonify({'message': 'Cannot delete your own account'}), 400
    
    success = firebase_service.delete_user(user_id)
    if not success:
        return jsonify({'message': 'Failed to delete user'}), 500
    
    return jsonify({'message': 'User deleted successfully'})
