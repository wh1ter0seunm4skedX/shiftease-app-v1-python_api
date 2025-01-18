import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Initialize Firebase Admin
cred = credentials.Certificate("../../firebase-credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Sample events data
events = [
    {
        "name": "Community Center Youth Night",
        "date": datetime.now() + timedelta(days=7),
        "location": "Main Community Center",
        "description": "Weekly youth activity night featuring games and workshops",
        "required_workers": 3,
        "registered_workers": [],
        "status": "active"
    },
    {
        "name": "Weekend Sports Program",
        "date": datetime.now() + timedelta(days=14),
        "location": "Community Sports Field",
        "description": "Sports activities and training for local youth",
        "required_workers": 4,
        "registered_workers": [],
        "status": "active"
    },
    {
        "name": "Art Workshop",
        "date": datetime.now() + timedelta(days=21),
        "location": "Creative Arts Room",
        "description": "Introduction to painting and drawing for beginners",
        "required_workers": 2,
        "registered_workers": [],
        "status": "active"
    }
]

# Add events to the database
for event in events:
    doc_ref = db.collection('events').add(event)
    print(f"Added event: {event['name']} with ID: {doc_ref[1].id}")

# Sample registrations data (we'll create these after getting some user IDs)
print("\nFetching users to create registrations...")
users = db.collection('users').stream()
user_ids = [user.id for user in users]

if user_ids:
    # Create some sample registrations
    for event_ref in db.collection('events').list_documents():
        for user_id in user_ids[:2]:  # Register first two users for each event
            registration = {
                "user_id": user_id,
                "event_id": event_ref.id,
                "status": "confirmed",
                "registration_timestamp": datetime.now(),
                "role": "general worker"
            }
            doc_ref = db.collection('registrations').add(registration)
            print(f"Added registration for user {user_id} to event {event_ref.id}")

print("\nDatabase initialization completed!")
