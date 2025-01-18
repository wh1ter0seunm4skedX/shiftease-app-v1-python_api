import requests

url = "http://127.0.0.1:5000/events"
event_data = {
    "name": "New Community Workshop",
    "date": "2025-01-25T10:00:00Z",
    "location": "Community Center Room A",
    "description": "A workshop for community engagement and skill development.",
    "required_workers": 5,
    "registered_workers": [],
    "status": "active"
}

response = requests.post(url, json=event_data)

if response.status_code == 201:
    print("Event created successfully:", response.json())
else:
    print("Failed to create event:", response.status_code, response.text)