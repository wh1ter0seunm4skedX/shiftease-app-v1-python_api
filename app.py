from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
from datetime import datetime
import jwt
from functools import wraps

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Firebase with better error handling
cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
if not cred_path or not os.path.exists(cred_path):
    print(f"Error: Firebase credentials file not found at {cred_path}")
    print("Please make sure to:")
    print("1. Create a Firebase project at https://console.firebase.google.com/")
    print("2. Download the service account key")
    print("3. Save it as 'firebase-credentials.json' in the project root")
    exit(1)

try:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Error initializing Firebase: {str(e)}")
    exit(1)

# Get JWT secret from environment
JWT_SECRET = os.getenv('JWT_SECRET')
if not JWT_SECRET:
    print("Error: JWT_SECRET not found in environment variables")
    exit(1)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer ' prefix
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user = db.collection('users').document(data['user_id']).get()
            if not current_user.exists:
                return jsonify({'message': 'Invalid token'}), 401
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            current_user = db.collection('users').document(data['user_id']).get()
            if not current_user.exists or current_user.to_dict()['role'] != 'manager':
                return jsonify({'message': 'Admin privileges required'}), 403
        except:
            return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    if not all(k in data for k in ['email', 'password', 'name', 'role']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    users_ref = db.collection('users')
    if users_ref.where('email', '==', data['email']).get():
        return jsonify({'message': 'User already exists'}), 400
    
    # Create new user
    new_user = {
        'email': data['email'],
        'name': data['name'],
        'role': data['role'],
        'created_at': datetime.utcnow().isoformat(),
        'password': data['password']  # In production, this should be hashed
    }
    
    user_ref = users_ref.add(new_user)
    return jsonify({'message': 'User created successfully', 'user_id': user_ref[1].id}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Find user
    users_ref = db.collection('users')
    user_query = users_ref.where('email', '==', data['email']).limit(1).get()
    
    if not user_query:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    user = user_query[0]
    user_data = user.to_dict()
    
    # In production, properly compare hashed passwords
    if user_data['password'] != data['password']:
        return jsonify({'message': 'Invalid credentials'}), 401
    
    # Generate JWT token
    token = jwt.encode({
        'user_id': user.id,
        'email': user_data['email'],
        'role': user_data['role']
    }, JWT_SECRET, algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'id': user.id,
            'email': user_data['email'],
            'name': user_data['name'],
            'role': user_data['role']
        }
    })

# Event routes
@app.route('/api/events', methods=['GET'])
@token_required
def get_events():
    events_ref = db.collection('events')
    events = [{'id': doc.id, **doc.to_dict()} for doc in events_ref.stream()]
    return jsonify(events)

@app.route('/api/events', methods=['POST'])
@admin_required
def create_event():
    data = request.json
    if not all(k in data for k in ['title', 'description', 'date', 'capacity']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    event_data = {
        'title': data['title'],
        'description': data['description'],
        'date': data['date'],
        'capacity': data['capacity'],
        'registered_users': [],
        'created_at': datetime.utcnow().isoformat()
    }
    
    event_ref = db.collection('events').add(event_data)
    return jsonify({'message': 'Event created successfully', 'event_id': event_ref[1].id}), 201

@app.route('/api/events/<event_id>', methods=['GET'])
@token_required
def get_event(event_id):
    event_ref = db.collection('events').document(event_id)
    event = event_ref.get()
    
    if not event.exists:
        return jsonify({'message': 'Event not found'}), 404
    
    return jsonify({'id': event.id, **event.to_dict()})

@app.route('/api/events/<event_id>', methods=['PUT'])
@admin_required
def update_event(event_id):
    data = request.json
    event_ref = db.collection('events').document(event_id)
    
    if not event_ref.get().exists:
        return jsonify({'message': 'Event not found'}), 404
    
    event_ref.update(data)
    return jsonify({'message': 'Event updated successfully'})

@app.route('/api/events/<event_id>', methods=['DELETE'])
@admin_required
def delete_event(event_id):
    event_ref = db.collection('events').document(event_id)
    
    if not event_ref.get().exists:
        return jsonify({'message': 'Event not found'}), 404
    
    event_ref.delete()
    return jsonify({'message': 'Event deleted successfully'})

# User routes
@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    users_ref = db.collection('users')
    users = [{'id': doc.id, **doc.to_dict()} for doc in users_ref.stream()]
    return jsonify(users)

@app.route('/api/users/<user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    user_ref = db.collection('users').document(user_id)
    user = user_ref.get()
    
    if not user.exists:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({'id': user.id, **user.to_dict()})

@app.route('/api/users/<user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    data = request.json
    user_ref = db.collection('users').document(user_id)
    
    if not user_ref.get().exists:
        return jsonify({'message': 'User not found'}), 404
    
    user_ref.update(data)
    return jsonify({'message': 'User updated successfully'})

@app.route('/api/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user_ref = db.collection('users').document(user_id)
    
    if not user_ref.get().exists:
        return jsonify({'message': 'User not found'}), 404
    
    user_ref.delete()
    return jsonify({'message': 'User deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
