from flask import Blueprint, request, jsonify, g
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
    if not all(k in data for k in ['title', 'description', 'date', 'required_workers']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    event = Event(
        title=data['title'],
        description=data['description'],
        date=data['date'],
        required_workers=data['required_workers']
    )
    
    event_id = firebase_service.create_event(event)
    if not event_id:
        return jsonify({'message': 'Failed to create event'}), 500
        
    return jsonify({
        'message': 'Event created successfully',
        'event_id': event_id
    }), 201

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
    if not any(k in data for k in ['title', 'description', 'date', 'required_workers']):
        return jsonify({'message': 'No fields to update'}), 400
    
    success = firebase_service.update_event(event_id, data)
    if not success:
        return jsonify({'message': 'Failed to update event'}), 500
        
    return jsonify({'message': 'Event updated successfully'})

@events_bp.route('/<event_id>', methods=['DELETE'])
@admin_required
def delete_event(event_id):
    success = firebase_service.delete_event(event_id)
    if not success:
        return jsonify({'message': 'Failed to delete event'}), 500
        
    return jsonify({'message': 'Event deleted successfully'})

@events_bp.route('/<event_id>/register', methods=['POST'])
@token_required
def register_for_event(event_id):
    event = firebase_service.get_event(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    if event.is_full():
        return jsonify({'message': 'Event is at full capacity'}), 400
        
    if event.is_user_registered(g.user.id):
        return jsonify({'message': 'Already registered for this event'}), 400
    
    success = firebase_service.register_worker(event_id, g.user.id)
    if not success:
        return jsonify({'message': 'Failed to register for event'}), 500
        
    return jsonify({'message': 'Successfully registered for event'})

@events_bp.route('/<event_id>/unregister', methods=['POST'])
@token_required
def unregister_from_event(event_id):
    event = firebase_service.get_event(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404
    
    if not event.is_user_registered(g.user.id):
        return jsonify({'message': 'Not registered for this event'}), 400
    
    success = firebase_service.unregister_worker(event_id, g.user.id)
    if not success:
        return jsonify({'message': 'Failed to unregister from event'}), 500
        
    return jsonify({'message': 'Successfully unregistered from event'})

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
