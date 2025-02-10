import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import json
from ..models.user import User
from ..models.event import Event

class FirebaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize Firebase connection or mock database for testing"""
        self.is_testing = os.getenv('TESTING', 'false').lower() == 'true'
        
        if self.is_testing:
            print("Running in test mode, using mock database")
            self._initialize_mock_db()
        else:
            try:
                # Get the absolute path to the credentials file
                creds_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
                print(f"Looking for Firebase credentials at: {creds_path}")
                
                if not creds_path:
                    raise ValueError("FIREBASE_CREDENTIALS_PATH environment variable not set")
                
                # Convert relative path to absolute path if necessary
                if not os.path.isabs(creds_path):
                    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                    creds_path = os.path.join(base_dir, creds_path)
                    print(f"Converted to absolute path: {creds_path}")
                
                if not os.path.exists(creds_path):
                    raise FileNotFoundError(f"Firebase credentials file not found at: {creds_path}")
                
                # Initialize Firebase if not already initialized
                if not firebase_admin._apps:
                    print("Initializing Firebase...")
                    cred = credentials.Certificate(creds_path)
                    firebase_admin.initialize_app(cred)
                    print("Firebase initialized successfully!")
                
                self.db = firestore.client()
                self.is_testing = False
                print("Successfully connected to Firestore!")
                
            except Exception as e:
                print(f"Error initializing Firebase: {str(e)}")
                print("Stack trace:", e.__traceback__)
                print("Falling back to mock database")
                self.is_testing = True
                self._initialize_mock_db()

    def _initialize_mock_db(self):
        """Initialize a mock database for testing"""
        print("Initializing mock database")
        self.mock_db = {
            'users': {},
            'events': {}
        }
        self.db = self.MockFirestore(self.mock_db)
        print("Mock database initialized")

    class MockFirestore:
        def __init__(self, mock_db):
            self.mock_db = mock_db

        def collection(self, collection_name):
            return FirebaseService.MockCollection(self.mock_db, collection_name)

    class MockCollection:
        def __init__(self, mock_db, collection_name):
            self.mock_db = mock_db
            self.collection_name = collection_name

        def document(self, doc_id=None):
            if doc_id is None:
                doc_id = str(len(self.mock_db[self.collection_name]) + 1)
            return FirebaseService.MockDocument(self.mock_db, self.collection_name, doc_id)

        def get(self):
            docs = []
            for doc_id, data in self.mock_db[self.collection_name].items():
                docs.append(FirebaseService.MockDocumentSnapshot(doc_id, data))
            return docs

        def where(self, field, op, value):
            filtered_docs = {}
            for doc_id, data in self.mock_db[self.collection_name].items():
                if field in data:
                    if op == '==' and data[field] == value:
                        filtered_docs[doc_id] = data
                    elif op == 'in' and data[field] in value:
                        filtered_docs[doc_id] = data
            return FirebaseService.MockQuery(filtered_docs)

    class MockDocument:
        def __init__(self, mock_db, collection_name, doc_id):
            self.mock_db = mock_db
            self.collection_name = collection_name
            self._id = doc_id

        @property
        def id(self):
            return self._id

        def set(self, data):
            self.mock_db[self.collection_name][self._id] = data

        def get(self):
            data = self.mock_db[self.collection_name].get(self._id)
            return FirebaseService.MockDocumentSnapshot(self._id, data)

        def update(self, data):
            if self._id in self.mock_db[self.collection_name]:
                self.mock_db[self.collection_name][self._id].update(data)

        def delete(self):
            if self._id in self.mock_db[self.collection_name]:
                del self.mock_db[self.collection_name][self._id]

    class MockDocumentSnapshot:
        def __init__(self, doc_id, data):
            self._id = doc_id
            self._data = data

        def to_dict(self):
            return self._data if self._data else None

        def exists(self):
            return self._data is not None

        @property
        def id(self):
            return self._id

    class MockQuery:
        def __init__(self, filtered_docs):
            self.filtered_docs = filtered_docs

        def get(self):
            return [FirebaseService.MockDocumentSnapshot(doc_id, data) 
                   for doc_id, data in self.filtered_docs.items()]

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
