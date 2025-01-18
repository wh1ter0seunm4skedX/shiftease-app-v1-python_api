from flask import Blueprint, request, jsonify
from ..services.firebase_service import FirebaseService
from ..services.auth_service import token_required, admin_required
from ..models.event import Event

events_bp = Blueprint('events', __name__)
firebase_service = FirebaseService()

@events_bp.route('/', methods=['GET'])
@token_required
def get_events():
    events = firebase_service.get_all_events()
    return jsonify([{
        'id': event.id,
        **event.to_dict()
    } for event in events])

@events_bp.route('/', methods=['POST'])
@admin_required
def create_event():
    data = request.json
    if not all(k in data for k in ['title', 'description', 'date', 'capacity']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    event = Event(
        title=data['title'],
        description=data['description'],
        date=data['date'],
        capacity=data['capacity']
    )
    
    event_id = firebase_service.create_event(event)
    return jsonify({'message': 'Event created successfully', 'event_id': event_id}), 201

@events_bp.route('/<event_id>', methods=['GET'])
@token_required
def get_event(event_id):
    event = firebase_service.get_event(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    return jsonify({
        'id': event.id,
        **event.to_dict()
    })

@events_bp.route('/<event_id>', methods=['PUT'])
@admin_required
def update_event(event_id):
    data = request.json
    event = firebase_service.get_event(event_id)
    
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    firebase_service.update_event(event_id, data)
    return jsonify({'message': 'Event updated successfully'})

@events_bp.route('/<event_id>', methods=['DELETE'])
@admin_required
def delete_event(event_id):
    event = firebase_service.get_event(event_id)
    
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    firebase_service.delete_event(event_id)
    return jsonify({'message': 'Event deleted successfully'})

@events_bp.route('/<event_id>/register', methods=['POST'])
@token_required
def register_for_event(event_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400
    
    event = firebase_service.get_event(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    if len(event.registered_users) >= event.capacity:
        return jsonify({'message': 'Event is full'}), 400
    
    firebase_service.register_for_event(event_id, user_id)
    return jsonify({'message': 'Successfully registered for event'})
