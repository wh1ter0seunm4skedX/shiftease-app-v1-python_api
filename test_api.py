import requests
import json
from datetime import datetime, timedelta

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
    
    # Store the token
    token = response.json().get('token')
    headers = {'Authorization': f'Bearer {token}'}
    
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
    
    # 4. Create an event
    print("\n4. Testing Event Creation...")
    event_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "date": (datetime.now() + timedelta(days=7)).isoformat(),
        "capacity": 10
    }
    response = requests.post(f"{BASE_URL}/events", json=event_data, headers=headers)
    print_response(response)
    
    # Store event ID
    event_id = response.json().get('event_id')
    
    # 5. Get all events
    print("\n5. Testing Get All Events...")
    response = requests.get(f"{BASE_URL}/events", headers=headers)
    print_response(response)
    
    # 6. Get specific event
    print("\n6. Testing Get Specific Event...")
    response = requests.get(f"{BASE_URL}/events/{event_id}", headers=headers)
    print_response(response)
    
    # 7. Update event
    print("\n7. Testing Event Update...")
    update_data = {
        "title": "Updated Test Event",
        "capacity": 15
    }
    response = requests.put(f"{BASE_URL}/events/{event_id}", json=update_data, headers=headers)
    print_response(response)
    
    # 8. Get all users (manager only)
    print("\n8. Testing Get All Users...")
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    print_response(response)
    
    # 9. Delete event
    print("\n9. Testing Event Deletion...")
    response = requests.delete(f"{BASE_URL}/events/{event_id}", headers=headers)
    print_response(response)

if __name__ == "__main__":
    try:
        test_api()
        print("\nAll tests completed!")
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"\nError during testing: {str(e)}")
