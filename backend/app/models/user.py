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
    def from_dict(data, user_id=None):
        """Create a User instance from a dictionary"""
        user = User(
            email=data.get('email'),
            name=data.get('name'),
            role=data.get('role'),
            password=data.get('password'),
            user_id=user_id or data.get('user_id')
        )
        user.created_at = data.get('created_at', datetime.utcnow().isoformat())
        return user
