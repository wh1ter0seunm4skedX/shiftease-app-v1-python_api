import unittest
import requests
import json
from datetime import datetime, timedelta
import os
import sys

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(backend_dir)

BASE_URL = 'http://localhost:5000/api'

class TestShiftEaseAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data and authenticate users"""
        # Create and authenticate manager
        cls.manager_data = {
            "email": "test.manager@shiftease.com",
            "password": "test123",
            "name": "Test Manager",
            "role": "manager"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=cls.manager_data)
        print(f"\nManager Registration Response: {response.status_code}")
        print(response.text)
        
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": cls.manager_data["email"],
            "password": cls.manager_data["password"]
        })
        print(f"\nManager Login Response: {response.status_code}")
        print(response.text)
        
        cls.manager_token = response.json()['token']
        cls.manager_headers = {'Authorization': f'Bearer {cls.manager_token}'}

        # Create and authenticate worker
        cls.worker_data = {
            "email": "test.worker@shiftease.com",
            "password": "test123",
            "name": "Test Worker",
            "role": "worker"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=cls.worker_data)
        print(f"\nWorker Registration Response: {response.status_code}")
        print(response.text)
        
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": cls.worker_data["email"],
            "password": cls.worker_data["password"]
        })
        print(f"\nWorker Login Response: {response.status_code}")
        print(response.text)
        
        cls.worker_token = response.json()['token']
        cls.worker_headers = {'Authorization': f'Bearer {cls.worker_token}'}

    def test_1_user_crud(self):
        """Test User CRUD operations"""
        print("\n=== Testing User CRUD Operations ===")
        
        # Create (Register) new worker
        print("\nTesting User Creation...")
        new_worker_data = {
            "email": "new.worker@shiftease.com",
            "password": "test123",
            "name": "New Test Worker",
            "role": "worker"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=new_worker_data)
        self.assertEqual(response.status_code, 201)
        print(f"Create User Response: {response.json()}")

        # Read (Get all users - manager only)
        print("\nTesting Get All Users...")
        response = requests.get(f"{BASE_URL}/users", headers=self.manager_headers)
        self.assertEqual(response.status_code, 200)
        users = response.json()
        self.assertTrue(len(users) >= 3)  # Manager, Worker, and New Worker
        print(f"Get Users Response: {json.dumps(users, indent=2)}")

        # Update user
        print("\nTesting User Update...")
        update_data = {"name": "Updated Worker Name"}
        response = requests.put(
            f"{BASE_URL}/users/{users[0]['id']}", 
            headers=self.manager_headers,
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        print(f"Update User Response: {response.json()}")

        # Delete user
        print("\nTesting User Deletion...")
        response = requests.delete(
            f"{BASE_URL}/users/{users[0]['id']}", 
            headers=self.manager_headers
        )
        self.assertEqual(response.status_code, 200)
        print(f"Delete User Response: {response.json()}")

    def test_2_event_crud(self):
        """Test Event CRUD operations"""
        print("\n=== Testing Event CRUD Operations ===")

        # Create event
        print("\nTesting Event Creation...")
        event_data = {
            "title": "Test Event",
            "description": "This is a test event",
            "date": (datetime.now() + timedelta(days=7)).isoformat(),
            "capacity": 3,
            "required_workers": 2
        }
        response = requests.post(
            f"{BASE_URL}/events", 
            headers=self.manager_headers,
            json=event_data
        )
        self.assertEqual(response.status_code, 201)
        event_id = response.json()['event_id']
        print(f"Create Event Response: {response.json()}")

        # Read (Get all events)
        print("\nTesting Get All Events...")
        response = requests.get(f"{BASE_URL}/events", headers=self.worker_headers)
        self.assertEqual(response.status_code, 200)
        events = response.json()
        self.assertTrue(len(events) >= 1)
        print(f"Get Events Response: {json.dumps(events, indent=2)}")

        # Read (Get specific event)
        print("\nTesting Get Specific Event...")
        response = requests.get(
            f"{BASE_URL}/events/{event_id}", 
            headers=self.worker_headers
        )
        self.assertEqual(response.status_code, 200)
        print(f"Get Event Response: {json.dumps(response.json(), indent=2)}")

        # Update event
        print("\nTesting Event Update...")
        update_data = {
            "title": "Updated Test Event",
            "required_workers": 3
        }
        response = requests.put(
            f"{BASE_URL}/events/{event_id}", 
            headers=self.manager_headers,
            json=update_data
        )
        self.assertEqual(response.status_code, 200)
        print(f"Update Event Response: {response.json()}")

        # Store event_id for registration tests
        self.event_id = event_id

    def test_3_event_registration(self):
        """Test Event Registration functionality"""
        print("\n=== Testing Event Registration ===")

        # Create additional workers for testing
        worker_data_list = [
            {
                "email": f"worker{i}@shiftease.com",
                "password": "test123",
                "name": f"Test Worker {i}",
                "role": "worker"
            }
            for i in range(1, 4)
        ]

        worker_tokens = []
        for worker_data in worker_data_list:
            # Register worker
            response = requests.post(f"{BASE_URL}/auth/register", json=worker_data)
            print(f"\nWorker Registration Response: {response.status_code}")
            print(response.text)
            
            # Login worker
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": worker_data["email"],
                "password": worker_data["password"]
            })
            print(f"\nWorker Login Response: {response.status_code}")
            print(response.text)
            
            worker_tokens.append(response.json()['token'])

        # Test registration for multiple workers
        print("\nTesting Multiple Worker Registrations...")
        for i, token in enumerate(worker_tokens):
            headers = {'Authorization': f'Bearer {token}'}
            response = requests.post(
                f"{BASE_URL}/events/{self.event_id}/register",
                headers=headers
            )
            print(f"Worker {i+1} Registration Response: {response.json()}")
            if i < 2:  # First two workers should succeed
                self.assertEqual(response.status_code, 200)
            else:  # Third worker should fail as we only need 2 workers
                self.assertEqual(response.status_code, 400)

        # Check event status
        print("\nChecking Event Status After Registrations...")
        response = requests.get(
            f"{BASE_URL}/events/{self.event_id}",
            headers=self.manager_headers
        )
        event_status = response.json()
        self.assertEqual(len(event_status['registered_users']), 2)
        print(f"Event Status: {json.dumps(event_status, indent=2)}")

        # Test unregistration
        print("\nTesting Worker Unregistration...")
        headers = {'Authorization': f'Bearer {worker_tokens[0]}'}
        response = requests.post(
            f"{BASE_URL}/events/{self.event_id}/unregister",
            headers=headers
        )
        self.assertEqual(response.status_code, 200)
        print(f"Unregister Response: {response.json()}")

        # Verify event needs one more worker after unregistration
        print("\nVerifying Event Needs One More Worker...")
        response = requests.get(
            f"{BASE_URL}/events/{self.event_id}",
            headers=self.manager_headers
        )
        event_status = response.json()
        self.assertEqual(len(event_status['registered_users']), 1)
        print(f"Final Event Status: {json.dumps(event_status, indent=2)}")

if __name__ == '__main__':
    try:
        unittest.main(verbosity=2)
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
