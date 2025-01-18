import requests
import json
from datetime import datetime, timedelta
import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = 'http://localhost:5000/api'

def print_response(response):
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
    print("-" * 50)

def test_api():
    # 1. Register a manager
    print("\n1. Testing Manager Registration...")
    manager_data = {
        "email": "manager@test.com",
        "password": "test123",
        "name": "Test Manager",
        "role": "manager"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=manager_data)
    print_response(response)
    
    # 2. Login as manager
    print("\n2. Testing Manager Login...")
    login_data = {
        "email": "manager@test.com",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response)
    
    # Store the manager token
    manager_token = response.json().get('token')
    manager_headers = {'Authorization': f'Bearer {manager_token}'}
    
    # 3. Register a worker
    print("\n3. Testing Worker Registration...")
    worker_data = {
        "email": "worker@test.com",
        "password": "test123",
        "name": "Test Worker",
        "role": "worker"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=worker_data)
    print_response(response)
    
    # 4. Login as worker
    print("\n4. Testing Worker Login...")
    login_data = {
        "email": "worker@test.com",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response)
    
    # Store the worker token
    worker_token = response.json().get('token')
    worker_headers = {'Authorization': f'Bearer {worker_token}'}
    
    # 5. Create an event as manager
    print("\n5. Testing Event Creation...")
    event_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "date": (datetime.now() + timedelta(days=7)).isoformat(),
        "capacity": 2
    }
    response = requests.post(f"{BASE_URL}/events", json=event_data, headers=manager_headers)
    print_response(response)
    
    # Store event ID
    event_id = response.json().get('event_id')
    
    # 6. Worker tries to register for the event
    print("\n6. Testing Event Registration...")
    response = requests.post(f"{BASE_URL}/events/{event_id}/register", headers=worker_headers)
    print_response(response)
    
    # 7. Get worker's registered events
    print("\n7. Testing Get My Events...")
    response = requests.get(f"{BASE_URL}/events/my-events", headers=worker_headers)
    print_response(response)
    
    # 8. Register another worker
    print("\n8. Testing Second Worker Registration...")
    worker2_data = {
        "email": "worker2@test.com",
        "password": "test123",
        "name": "Test Worker 2",
        "role": "worker"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=worker2_data)
    print_response(response)
    
    # 9. Login as second worker
    print("\n9. Testing Second Worker Login...")
    login_data = {
        "email": "worker2@test.com",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response)
    
    worker2_token = response.json().get('token')
    worker2_headers = {'Authorization': f'Bearer {worker2_token}'}
    
    # 10. Second worker registers for the event
    print("\n10. Testing Second Worker Event Registration...")
    response = requests.post(f"{BASE_URL}/events/{event_id}/register", headers=worker2_headers)
    print_response(response)
    
    # 11. Try to register a third worker (should fail due to capacity)
    print("\n11. Testing Third Worker Registration (Should Fail)...")
    worker3_data = {
        "email": "worker3@test.com",
        "password": "test123",
        "name": "Test Worker 3",
        "role": "worker"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=worker3_data)
    print_response(response)
    
    login_data = {
        "email": "worker3@test.com",
        "password": "test123"
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    worker3_token = response.json().get('token')
    worker3_headers = {'Authorization': f'Bearer {worker3_token}'}
    
    response = requests.post(f"{BASE_URL}/events/{event_id}/register", headers=worker3_headers)
    print_response(response)
    
    # 12. First worker unregisters from the event
    print("\n12. Testing Event Unregistration...")
    response = requests.post(f"{BASE_URL}/events/{event_id}/unregister", headers=worker_headers)
    print_response(response)
    
    # 13. Get all events as manager to verify registrations
    print("\n13. Testing Get All Events (as manager)...")
    response = requests.get(f"{BASE_URL}/events", headers=manager_headers)
    print_response(response)

if __name__ == "__main__":
    try:
        test_api()
        print("\nAll tests completed!")
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
