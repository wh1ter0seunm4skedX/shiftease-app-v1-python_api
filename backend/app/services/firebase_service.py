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
            # First get the Firebase Auth user
            auth_user = auth.get_user(uid)
            
            # Then get the user document from Firestore
            db = firestore.client()
            user_doc = db.collection('users').document(uid).get()
            
            if user_doc.exists:
                user_data = user_doc.to_dict()
                return User(
                    id=uid,
                    email=auth_user.email,
                    name=user_data.get('name', ''),
                    role=user_data.get('role', 'worker')
                )
            return None
        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None

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

    # User operations
    def create_user(self, user: User):
        """Create a new user document"""
        if self.is_testing:
            user_id = str(len(self.mock_db['users']) + 1)
            self.mock_db['users'][user_id] = user.to_dict()
            return user_id
        else:
            doc_ref = self.db.collection('users').document()
            user_data = user.to_dict()
            doc_ref.set(user_data)
            return doc_ref.id

    def get_user(self, user_id: str) -> User:
        """Get user by ID"""
        if self.is_testing:
            if user_id not in self.mock_db['users']:
                return None
            user_data = self.mock_db['users'][user_id]
            return User.from_dict(user_data)
        else:
            doc_ref = self.db.collection('users').document(user_id)
            doc = doc_ref.get()
            if not doc.exists:
                return None
            user_data = doc.to_dict()
            user_data['user_id'] = doc.id
            return User.from_dict(user_data)

    def get_user_by_email(self, email: str):
        """Get user by email"""
        users_ref = self.db.collection('users')
        query = users_ref.where('email', '==', email).get()
        for user in query:
            return User.from_dict(user.to_dict(), user.id)
        return None

    def get_all_users(self):
        """Get all users"""
        users = []
        for doc in self.db.collection('users').get():
            users.append(User.from_dict(doc.to_dict(), doc.id))
        return users

    def update_user(self, user_id: str, data: dict):
        """Update user document"""
        user_ref = self.db.collection('users').document(user_id)
        user_ref.update(data)

    def delete_user(self, user_id: str):
        """Delete user document"""
        self.db.collection('users').document(user_id).delete()

    # Event operations
    def create_event(self, event: Event):
        """Create a new event document"""
        if self.is_testing:
            event_id = str(len(self.mock_db['events']) + 1)
            self.mock_db['events'][event_id] = event.to_dict()
            return event_id
        else:
            doc_ref = self.db.collection('events').document()
            event_data = event.to_dict()
            doc_ref.set(event_data)
            return doc_ref.id

    def get_event(self, event_id: str) -> Event:
        """Get event by ID"""
        if self.is_testing:
            if event_id not in self.mock_db['events']:
                return None
            event_data = self.mock_db['events'][event_id]
            return Event.from_dict(event_data)
        else:
            doc_ref = self.db.collection('events').document(event_id)
            doc = doc_ref.get()
            if not doc.exists:
                return None
            event_data = doc.to_dict()
            event_data['event_id'] = doc.id
            return Event.from_dict(event_data)

    def get_all_events(self):
        """Get all events"""
        events = []
        for doc in self.db.collection('events').get():
            events.append(Event.from_dict(doc.to_dict(), doc.id))
        return events

    def update_event(self, event_id: str, data: dict):
        """Update event document"""
        event_ref = self.db.collection('events').document(event_id)
        event_ref.update(data)

    def delete_event(self, event_id: str):
        """Delete event document"""
        self.db.collection('events').document(event_id).delete()

    def register_for_event(self, event_id: str, user_id: str):
        """Register a user for an event"""
        event_ref = self.db.collection('events').document(event_id)
        event_ref.update({
            'registered_users': firestore.ArrayUnion([user_id])
        })

    def unregister_from_event(self, event_id: str, user_id: str):
        """Unregister a user from an event"""
        event_ref = self.db.collection('events').document(event_id)
        event_ref.update({
            'registered_users': firestore.ArrayRemove([user_id])
        })

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
