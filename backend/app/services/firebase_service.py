import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from datetime import datetime
import json
from ..models.user import User
from ..models.event import Event
from functools import wraps
from flask import request, jsonify

class FirebaseService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            try:
                firebase_admin.get_app()
            except ValueError:
                # Use the credentials file from the config directory
                creds_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config', 'firebase-credentials.json')
                if not os.path.exists(creds_path):
                    raise FileNotFoundError(f"Firebase credentials file not found at: {creds_path}")
                
                print(f"Initializing Firebase with credentials from: {creds_path}")
                cred = credentials.Certificate(creds_path)
                firebase_admin.initialize_app(cred)
            
            # Initialize Firestore
            cls._instance.db = firestore.client()
                
        return cls._instance

    def verify_token(self, id_token):
        """
        Verify the Firebase ID token
        :param id_token: The Firebase ID token to verify
        :return: The decoded token if valid, None otherwise
        """
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            print(f"Token verification error: {str(e)}")
            return None

    def get_user_by_id(self, uid):
        """
        Get a user from Firestore by their UID
        :param uid: The user's UID
        :return: User object if found, None otherwise
        """
        try:
            # Get user data from Firestore
            user_doc = self.db.collection('users').document(uid).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                return User(
                    id=uid,
                    email=user_data.get('email'),
                    name=user_data.get('name'),
                    role=user_data.get('role', 'worker')  # Default to worker if role not set
                )
            return None
        except Exception as e:
            print(f"Error getting user by ID: {str(e)}")
            return None

    def get_all_events(self):
        """
        Get all events from Firestore
        :return: List of Event objects
        """
        try:
            events = []
            events_ref = self.db.collection('events').stream()
            
            for event_doc in events_ref:
                event_data = event_doc.to_dict()
                event = Event(
                    id=event_doc.id,
                    title=event_data.get('title'),
                    description=event_data.get('description'),
                    date=event_data.get('date'),
                    required_workers=event_data.get('required_workers', 0),
                    registered_workers=event_data.get('registered_workers', [])
                )
                events.append(event)
            
            return events
        except Exception as e:
            print(f"Error getting all events: {str(e)}")
            return []

    def get_event(self, event_id):
        """
        Get an event from Firestore by ID
        :param event_id: The event's ID
        :return: Event object if found, None otherwise
        """
        try:
            event_doc = self.db.collection('events').document(event_id).get()
            if event_doc.exists:
                event_data = event_doc.to_dict()
                return Event(
                    id=event_id,
                    title=event_data.get('title'),
                    description=event_data.get('description'),
                    date=event_data.get('date'),
                    required_workers=event_data.get('required_workers', 0),
                    registered_workers=event_data.get('registered_workers', [])
                )
            return None
        except Exception as e:
            print(f"Error getting event: {str(e)}")
            return None

    def create_event(self, event):
        """
        Create a new event in Firestore
        :param event: Event object
        :return: Event ID if successful, None otherwise
        """
        try:
            event_ref = self.db.collection('events').document()
            event_ref.set({
                'title': event.title,
                'description': event.description,
                'date': event.date,
                'required_workers': event.required_workers,
                'registered_workers': [],
                'created_at': firestore.SERVER_TIMESTAMP
            })
            return event_ref.id
        except Exception as e:
            print(f"Error creating event: {str(e)}")
            return None

    def update_event(self, event_id, event_data):
        """
        Update an event in Firestore
        :param event_id: The event's ID
        :param event_data: Dictionary of fields to update
        :return: True if successful, False otherwise
        """
        try:
            event_ref = self.db.collection('events').document(event_id)
            event_ref.update({
                **event_data,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            return True
        except Exception as e:
            print(f"Error updating event: {str(e)}")
            return False

    def delete_event(self, event_id):
        """
        Delete an event from Firestore
        :param event_id: The event's ID
        :return: True if successful, False otherwise
        """
        try:
            self.db.collection('events').document(event_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting event: {str(e)}")
            return False

    def register_worker(self, event_id, user_id):
        """
        Register a worker for an event
        :param event_id: The event's ID
        :param user_id: The user's ID
        :return: True if successful, False otherwise
        """
        try:
            event_ref = self.db.collection('events').document(event_id)
            event_ref.update({
                'registered_workers': firestore.ArrayUnion([user_id])
            })
            return True
        except Exception as e:
            print(f"Error registering worker: {str(e)}")
            return False

    def unregister_worker(self, event_id, user_id):
        """
        Unregister a worker from an event
        :param event_id: The event's ID
        :param user_id: The user's ID
        :return: True if successful, False otherwise
        """
        try:
            event_ref = self.db.collection('events').document(event_id)
            event_ref.update({
                'registered_workers': firestore.ArrayRemove([user_id])
            })
            return True
        except Exception as e:
            print(f"Error unregistering worker: {str(e)}")
            return False

    def create_user(self, user: User):
        """
        Create a new user in Firestore
        :param user: User object
        :return: None
        """
        try:
            db = firestore.client()
            user_ref = db.collection('users').document(user.id)
            user_ref.set({
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'created_at': firestore.SERVER_TIMESTAMP
            })
            
            # Set custom claims for role-based access
            auth.set_custom_user_claims(user.id, {'role': user.role})
            
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            raise

    def update_user(self, user: User):
        """
        Update a user in Firestore
        :param user: User object
        :return: None
        """
        try:
            db = firestore.client()
            user_ref = db.collection('users').document(user.id)
            user_ref.update({
                'name': user.name,
                'role': user.role,
                'updated_at': firestore.SERVER_TIMESTAMP
            })
            
            # Update custom claims
            auth.set_custom_user_claims(user.id, {'role': user.role})
            
        except Exception as e:
            print(f"Error updating user: {str(e)}")
            raise

    def get_user_by_uid(self, uid):
        """
        Get a user by their UID
        :param uid: The user's UID
        :return: The user record if found, None otherwise
        """
        try:
            return auth.get_user(uid)
        except auth.UserNotFoundError:
            return None
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None

    def create_user_auth(self, email, password):
        """
        Create a new Firebase user
        :param email: User's email
        :param password: User's password
        :return: The created user record
        """
        try:
            user = auth.create_user(
                email=email,
                password=password
            )
            return user
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            raise

    def set_custom_claims(self, uid, claims):
        """
        Set custom claims for a user
        :param uid: The user's UID
        :param claims: Dictionary of custom claims
        """
        try:
            auth.set_custom_user_claims(uid, claims)
            return True
        except Exception as e:
            print(f"Error setting custom claims: {str(e)}")
            return False

def firebase_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'No token provided'}), 401

        token = auth_header.split('Bearer ')[1]
        firebase_service = FirebaseService()
        decoded_token = firebase_service.verify_token(token)

        if not decoded_token:
            return jsonify({'message': 'Invalid token'}), 401

        # Add the decoded token to the request context
        request.firebase_user = decoded_token
        return f(*args, **kwargs)

    return decorated_function
