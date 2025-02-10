def test_event_capacity_limit(self):
    """Test event registration capacity limits"""
    # Create multiple worker users
    workers = []
    for i in range(3):  # Create 3 workers
        worker_data = {
            "email": f"test.worker{i}@shiftease.com",
            "password": "test123",
            "name": f"Test Worker {i}",
            "role": "worker"
        }
        # Register the worker
        reg_response = requests.post(f"{self.BASE_URL}/auth/register", json=worker_data)
        if reg_response.status_code == 201:
            print(f"\nCreated worker: {worker_data['email']}")
        
        # Login as the worker to get their token
        login_response = requests.post(f"{self.BASE_URL}/auth/login", json={
            "email": worker_data["email"],
            "password": worker_data["password"]
        })
        self.assertEqual(login_response.status_code, 200, f"Failed to login as worker: {login_response.text}")
        workers.append({
            "email": worker_data["email"],
            "token": login_response.json()["token"]
        })

    # Create an event with capacity of 2
    event_data = {
        "title": "Limited Capacity Event",
        "description": "This event has limited capacity",
        "date": "2025-02-01T14:00:00Z",
        "capacity": 2  # Only 2 workers can register
    }
    
    # Create event using manager's token (from setUp)
    create_response = requests.post(
        f"{self.BASE_URL}/events/",
        headers=self.headers,
        json=event_data
    )
    self.assertEqual(create_response.status_code, 201, f"Failed to create event: {create_response.text}")
    event_id = create_response.json()["event_id"]
    print(f"\nCreated event with ID: {event_id}")

    # Try to register all workers (should succeed for first 2, fail for 3rd)
    for i, worker in enumerate(workers):
        register_response = requests.post(
            f"{self.BASE_URL}/events/{event_id}/register",
            headers={"Authorization": f"Bearer {worker['token']}"}
        )
        
        if i < 2:  # First two registrations should succeed
            self.assertEqual(
                register_response.status_code, 200,
                f"Registration should succeed for worker {i}: {register_response.text}"
            )
            print(f"\nSuccessfully registered worker: {worker['email']}")
        else:  # Third registration should fail
            self.assertEqual(
                register_response.status_code, 400,
                f"Registration should fail for worker {i} due to capacity limit"
            )
            self.assertIn("capacity", register_response.json().get("message", "").lower())
            print(f"\nCorrectly rejected registration for: {worker['email']} (capacity full)")

    # Verify event registration count
    event_response = requests.get(
        f"{self.BASE_URL}/events/{event_id}",
        headers=self.headers
    )
    self.assertEqual(event_response.status_code, 200)
    event = event_response.json()
    self.assertEqual(
        len(event.get("registered_workers", [])), 2,
        "Event should have exactly 2 registered workers"
    )
    print(f"\nFinal event registration count: {len(event.get('registered_workers', []))}")