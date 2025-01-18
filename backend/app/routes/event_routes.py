from flask import Blueprint, request, jsonify, g
from ..services.firebase_service import FirebaseService
from ..services.auth_service import token_required, admin_required, get_current_user
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
    current_user = get_current_user()
    
    if current_user['role'] != 'worker':
        return jsonify({'message': 'Only workers can register for events'}), 403
    
    event = firebase_service.get_event(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    try:
        event.register_user(current_user['user_id'])
        firebase_service.update_event(event_id, {'registered_users': event.registered_users})
        return jsonify({'message': 'Successfully registered for event'})
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@events_bp.route('/<event_id>/unregister', methods=['POST'])
@token_required
def unregister_from_event(event_id):
    current_user = get_current_user()
    
    if current_user['role'] != 'worker':
        return jsonify({'message': 'Only workers can unregister from events'}), 403
    
    event = firebase_service.get_event(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    try:
        event.unregister_user(current_user['user_id'])
        firebase_service.update_event(event_id, {'registered_users': event.registered_users})
        return jsonify({'message': 'Successfully unregistered from event'})
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@events_bp.route('/my-events', methods=['GET'])
@token_required
def get_my_events():
    current_user = get_current_user()
    
    if current_user['role'] != 'worker':
        return jsonify({'message': 'Only workers can view their registered events'}), 403
    
    events = firebase_service.get_all_events()
    my_events = [
        {
            'id': event.id,
            **event.to_dict()
        }
        for event in events
        if event.is_user_registered(current_user['user_id'])
    ]
    
    return jsonify(my_events)
