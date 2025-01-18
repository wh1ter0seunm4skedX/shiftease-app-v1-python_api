from datetime import datetime

class Event:
    def __init__(self, title, description, date, capacity, required_workers=None, event_id=None):
        self.id = event_id
        self.title = title
        self.description = description
        self.date = date
        self.capacity = capacity
        self.required_workers = required_workers or capacity  # If not specified, assume all capacity slots are required
        self.registered_users = []
        self.created_at = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'capacity': self.capacity,
            'required_workers': self.required_workers,
            'registered_users': self.registered_users,
            'created_at': self.created_at,
            'needs_workers': self.needs_workers()
        }
    
    @staticmethod
    def from_dict(source, event_id=None):
        event = Event(
            event_id=event_id,
            title=source.get('title'),
            description=source.get('description'),
            date=source.get('date'),
            capacity=source.get('capacity'),
            required_workers=source.get('required_workers')
        )
        if 'registered_users' in source:
            event.registered_users = source['registered_users']
        if 'created_at' in source:
            event.created_at = source['created_at']
        return event

    def is_full(self):
        return len(self.registered_users) >= self.capacity

    def needs_workers(self):
        """Check if the event still needs workers"""
        return len(self.registered_users) < self.required_workers

    def is_user_registered(self, user_id):
        return user_id in self.registered_users

    def register_user(self, user_id):
        if self.is_full():
            raise ValueError("Event is at full capacity")
        if self.is_user_registered(user_id):
            raise ValueError("User is already registered for this event")
        if not self.needs_workers():
            raise ValueError("Event has all required workers")
        self.registered_users.append(user_id)

    def unregister_user(self, user_id):
        if not self.is_user_registered(user_id):
            raise ValueError("User is not registered for this event")
        self.registered_users.remove(user_id)
