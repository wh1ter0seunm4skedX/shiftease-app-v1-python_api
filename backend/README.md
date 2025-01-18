# ShiftEase Backend

This is the backend service for ShiftEase, a modern web-based platform for managing event registration and attendance tracking for youth workers in community centers.

## Project Structure

```
backend/
├── app/
│   ├── models/
│   │   ├── user.py
│   │   └── event.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── event_routes.py
│   │   └── user_routes.py
│   ├── services/
│   │   ├── firebase_service.py
│   │   └── auth_service.py
│   ├── utils/
│   └── __init__.py
├── config/
│   └── config.py
├── tests/
│   └── test_api.py
├── requirements.txt
└── run.py
```

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Firebase:
   - Create a Firebase project at https://console.firebase.google.com/
   - Download the service account key
   - Save it as `firebase-credentials.json` in the project root

4. Create a `.env` file with the following variables:
   ```
   FLASK_APP=run.py
   FLASK_ENV=development
   FIREBASE_CREDENTIALS_PATH=../firebase-credentials.json
   JWT_SECRET=your-secure-secret-key
   ```

5. Run the application:
   ```bash
   python run.py
   ```

## API Documentation

### Authentication
- POST /api/auth/register - Register a new user
- POST /api/auth/login - Login and get JWT token

### Events
- GET /api/events - Get all events
- POST /api/events - Create a new event (manager only)
- GET /api/events/{event_id} - Get specific event
- PUT /api/events/{event_id} - Update event (manager only)
- DELETE /api/events/{event_id} - Delete event (manager only)
- POST /api/events/{event_id}/register - Register for an event

### Users
- GET /api/users - Get all users (manager only)
- GET /api/users/{user_id} - Get specific user (manager only)
- PUT /api/users/{user_id} - Update user (manager only)
- DELETE /api/users/{user_id} - Delete user (manager only)

## Testing

Run the tests using:
```bash
python -m pytest tests/
```

## Security Notes

- JWT tokens are used for authentication
- Role-based access control is implemented
- In production, passwords should be hashed before storage
