import unittest
import requests
import json

class TestServer(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/api"
    TEST_USER = {
        "email": "test.manager@shiftease.com",
        "password": "test123",
        "name": "Test Manager",
        "role": "manager"
    }

    def setUp(self):
        """Set up test case - register and get authentication token"""
        # Try to register (might fail if user exists, that's OK)
        requests.post(f"{self.BASE_URL}/auth/register", json=self.TEST_USER)
        
        # Login to get token
        login_data = {
            "email": self.TEST_USER["email"],
            "password": self.TEST_USER["password"]
        }
        response = requests.post(f"{self.BASE_URL}/auth/login", json=login_data)
        self.assertEqual(response.status_code, 200, f"Login failed: {response.text}")
        
        data = response.json()
        self.token = data['token']
        self.headers = {'Authorization': f'Bearer {self.token}'}
        print(f"\nLogged in as: {data['user']['email']}")

    def test_get_events(self):
        """Test getting all events"""
        response = requests.get(f"{self.BASE_URL}/events/", headers=self.headers)
        self.assertEqual(response.status_code, 200, f"Failed to get events: {response.text}")
        events = response.json()
        self.assertIsInstance(events, list)
        print(f"\nEvents retrieved: {json.dumps(events, indent=2)}")

    def test_get_users(self):
        """Test getting all users"""
        response = requests.get(f"{self.BASE_URL}/users/", headers=self.headers)
        self.assertEqual(response.status_code, 200, f"Failed to get users: {response.text}")
        users = response.json()
        self.assertIsInstance(users, list)
        print(f"\nUsers retrieved: {json.dumps(users, indent=2)}")

        def test_create_event(self):
            """Test creating a new event"""
            event_data = {
                "title": "Test Event",  # Changed from 'name' to 'title'
                "description": "Test Description",
                "date": "2025-02-01T14:00:00Z",
                "capacity": 10  # Changed from 'required_workers' to 'capacity'
            }
            response = requests.post(f"{self.BASE_URL}/events/", 
                                   headers=self.headers,
                                   json=event_data)
            self.assertEqual(response.status_code, 201, f"Failed to create event: {response.text}")
            created_event = response.json()
            self.assertIn('event_id', created_event)  # Changed from 'id' to 'event_id'
            print(f"\nCreated event: {json.dumps(created_event, indent=2)}")

if __name__ == '__main__':
    unittest.main()