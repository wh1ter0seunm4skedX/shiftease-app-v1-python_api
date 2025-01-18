from datetime import datetime

class Event:
    def __init__(self, title, description, date, capacity, event_id=None):
        self.id = event_id
        self.title = title
        self.description = description
        self.date = date
        self.capacity = capacity
        self.registered_users = []
        self.created_at = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'date': self.date,
            'capacity': self.capacity,
            'registered_users': self.registered_users,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(source, event_id=None):
        event = Event(
            event_id=event_id,
            title=source.get('title'),
            description=source.get('description'),
            date=source.get('date'),
            capacity=source.get('capacity')
        )
        if 'registered_users' in source:
            event.registered_users = source['registered_users']
        if 'created_at' in source:
            event.created_at = source['created_at']
        return event
