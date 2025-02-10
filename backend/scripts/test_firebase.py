import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.firebase_service import FirebaseService
from app.models.user import User
from app.models.event import Event
from datetime import datetime, timedelta

def test_firebase_connection():
    # Initialize Firebase service
    firebase_service = FirebaseService()
    
    try:
        # Test User Operations
        print("\n=== Testing User Operations ===")
        # Create a test user
        test_user = User(
            email="test@example.com",
            name="Test User",
            role="volunteer"
        )
        user_id = firebase_service.create_user(test_user)
        print(f"Created user with ID: {user_id}")
        
        # Retrieve the user
        retrieved_user = firebase_service.get_user(user_id)
        print(f"Retrieved user: {retrieved_user.to_dict()}")
        
        # Test Event Operations
        print("\n=== Testing Event Operations ===")
        # Create a test event
        test_event = Event(
            title="Test Event",
            description="A test event",
            date=(datetime.utcnow() + timedelta(days=7)).isoformat(),
            capacity=10
        )
        event_id = firebase_service.create_event(test_event)
        print(f"Created event with ID: {event_id}")
        
        # Retrieve the event
        retrieved_event = firebase_service.get_event(event_id)
        print(f"Retrieved event: {retrieved_event.to_dict()}")
        
        # Test registration
        print("\n=== Testing Event Registration ===")
        firebase_service.register_for_event(event_id, user_id)
        print(f"Registered user {user_id} for event {event_id}")
        
        # Clean up
        print("\n=== Cleaning Up ===")
        firebase_service.delete_event(event_id)
        firebase_service.delete_user(user_id)
        print("Test data cleaned up")
        
        print("\nAll tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    test_firebase_connection()
