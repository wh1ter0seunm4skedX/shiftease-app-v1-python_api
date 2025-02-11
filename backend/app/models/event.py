from datetime import datetime

class Event:
    def __init__(self, title, description, date, required_workers, event_id=None):
        self.id = event_id
        self.title = title
        self.description = description
        self.date = date
        self.required_workers = required_workers  
        self.registered_users = []
        self.created_at = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'required_workers': self.required_workers,
            'registered_users': self.registered_users,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data, event_id=None):
        """Create an Event instance from a dictionary"""
        event = Event(
            title=data.get('title'),
            description=data.get('description'),
            date=data.get('date'),
            required_workers=data.get('required_workers'),
            event_id=event_id or data.get('event_id')
        )
        event.registered_users = data.get('registered_users', [])
        event.created_at = data.get('created_at', datetime.utcnow().isoformat())
        return event

    def is_full(self):
        return len(self.registered_users) >= self.required_workers

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
