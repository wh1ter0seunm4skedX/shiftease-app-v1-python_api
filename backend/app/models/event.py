from datetime import datetime

class Event:
    def __init__(self, title, description, date, required_workers, id=None, registered_workers=None):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.required_workers = required_workers
        self.registered_workers = registered_workers or []
        self.created_at = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'required_workers': self.required_workers,
            'registered_workers': self.registered_workers,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(data, id=None):
        """Create an Event instance from a dictionary"""
        event = Event(
            title=data.get('title'),
            description=data.get('description'),
            date=data.get('date'),
            required_workers=data.get('required_workers'),
            id=id or data.get('id'),
            registered_workers=data.get('registered_workers', [])
        )
        event.created_at = data.get('created_at', datetime.utcnow().isoformat())
        return event

    def is_full(self):
        return len(self.registered_workers) >= self.required_workers

    def needs_workers(self):
        """Check if the event still needs workers"""
        return len(self.registered_workers) < self.required_workers

    def is_user_registered(self, user_id):
        return user_id in self.registered_workers

    def register_worker(self, user_id):
        if self.is_full():
            raise ValueError("Event is at full capacity")
        if self.is_user_registered(user_id):
            raise ValueError("Worker is already registered for this event")
        self.registered_workers.append(user_id)

    def unregister_worker(self, user_id):
        if not self.is_user_registered(user_id):
            raise ValueError("Worker is not registered for this event")
        self.registered_workers.remove(user_id)
