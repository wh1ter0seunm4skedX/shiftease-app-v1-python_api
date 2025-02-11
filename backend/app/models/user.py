from datetime import datetime
from typing import Optional, List

class User:
    def __init__(self, id: str, email: str, name: str, role: str = 'worker',
                 created_at: Optional[datetime] = None, last_login: Optional[datetime] = None,
                 registered_events: Optional[List[str]] = None):
        self.id = id  # Firebase UID
        self.email = email
        self.name = name
        self.role = role
        self.created_at = created_at or datetime.utcnow()
        self.last_login = last_login
        self.registered_events = registered_events or []

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'last_login': self.last_login.isoformat() if isinstance(self.last_login, datetime) else self.last_login,
            'registered_events': self.registered_events
        }

    @staticmethod
    def from_dict(data: dict, id: str = None):
        return User(
            id=data.get('id', id),
            email=data.get('email'),
            name=data.get('name'),
            role=data.get('role', 'worker'),
            created_at=data.get('created_at'),
            last_login=data.get('last_login'),
            registered_events=data.get('registered_events', [])
        )

    def is_admin(self):
        return self.role == 'admin'

    def is_worker(self):
        return self.role == 'worker'

    def register_event(self, event_id: str):
        if event_id not in self.registered_events:
            self.registered_events.append(event_id)

    def unregister_event(self, event_id: str):
        if event_id in self.registered_events:
            self.registered_events.remove(event_id)
