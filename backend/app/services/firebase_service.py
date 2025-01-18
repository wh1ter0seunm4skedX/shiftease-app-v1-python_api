import firebase_admin
from firebase_admin import credentials, firestore
from ..models.user import User
from ..models.event import Event
import os

class FirebaseService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH'))
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    # User operations
    def create_user(self, user: User):
        user_ref = self.db.collection('users').add(user.to_dict())
        return user_ref[1].id

    def get_user(self, user_id: str):
        user_doc = self.db.collection('users').document(user_id).get()
        if user_doc.exists:
            return User.from_dict(user_doc.to_dict(), user_id)
        return None

    def get_user_by_email(self, email: str):
        users = self.db.collection('users').where('email', '==', email).limit(1).get()
        for user in users:
            return User.from_dict(user.to_dict(), user.id)
        return None

    def get_all_users(self):
        users = []
        for doc in self.db.collection('users').stream():
            users.append(User.from_dict(doc.to_dict(), doc.id))
        return users

    def update_user(self, user_id: str, data: dict):
        self.db.collection('users').document(user_id).update(data)

    def delete_user(self, user_id: str):
        self.db.collection('users').document(user_id).delete()

    # Event operations
    def create_event(self, event: Event):
        event_ref = self.db.collection('events').add(event.to_dict())
        return event_ref[1].id

    def get_event(self, event_id: str):
        event_doc = self.db.collection('events').document(event_id).get()
        if event_doc.exists:
            return Event.from_dict(event_doc.to_dict(), event_id)
        return None

    def get_all_events(self):
        events = []
        for doc in self.db.collection('events').stream():
            events.append(Event.from_dict(doc.to_dict(), doc.id))
        return events

    def update_event(self, event_id: str, data: dict):
        self.db.collection('events').document(event_id).update(data)

    def delete_event(self, event_id: str):
        self.db.collection('events').document(event_id).delete()

    def register_for_event(self, event_id: str, user_id: str):
        event_ref = self.db.collection('events').document(event_id)
        event_ref.update({
            'registered_users': firestore.ArrayUnion([user_id])
        })
