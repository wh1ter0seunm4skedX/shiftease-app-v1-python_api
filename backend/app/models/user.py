from datetime import datetime

class User:
    def __init__(self, email, name, role, password=None, user_id=None):
        self.id = user_id
        self.email = email
        self.name = name
        self.role = role
        self.password = password
        self.created_at = datetime.utcnow().isoformat()
    
    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'password': self.password,
            'created_at': self.created_at
        }
    
    @staticmethod
    def from_dict(source, user_id=None):
        user = User(
            user_id=user_id,
            email=source.get('email'),
            name=source.get('name'),
            role=source.get('role'),
            password=source.get('password')
        )
        if 'created_at' in source:
            user.created_at = source['created_at']
        return user
