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
            self._initialize_mock_db()
        else:
            try:
                cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH'))
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
            except Exception as e:
                print(f"Warning: Could not initialize Firebase. Using mock database. Error: {str(e)}")
                self._initialize_mock_db()

    def _initialize_mock_db(self):
        """Initialize a mock database for testing"""
        self.mock_db = {
            'users': {},
            'events': {}
        }
        self.db = self.MockFirestore(self.mock_db)

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
        users_ref = self.db.collection('users')
        user_doc = users_ref.document()
        user_data = user.to_dict()
        user_data['id'] = user_doc.id
        user_data['created_at'] = datetime.now().isoformat()
        user_doc.set(user_data)
        return user_data

    def get_user(self, user_id: str):
        """Get user by ID"""
        user_doc = self.db.collection('users').document(user_id).get()
        if user_doc.exists:
            return User.from_dict(user_doc.to_dict(), user_id)
        return None

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
        events_ref = self.db.collection('events')
        event_doc = events_ref.document()
        event_data = event.to_dict()
        event_data['id'] = event_doc.id
        event_data['created_at'] = datetime.now().isoformat()
        event_data['registered_users'] = []
        event_doc.set(event_data)
        return event_data

    def get_event(self, event_id: str):
        """Get event by ID"""
        event_doc = self.db.collection('events').document(event_id).get()
        if event_doc.exists:
            return Event.from_dict(event_doc.to_dict(), event_id)
        return None

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
