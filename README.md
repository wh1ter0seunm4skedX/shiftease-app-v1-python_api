# ShiftEase

A modern web-based platform for managing event registration and attendance tracking for youth workers in community centers.

## Features

- Event management (CRUD operations)
- User management (CRUD operations)
- Role-based access control (Managers and Workers)
- Event registration and attendance tracking
- Automated notifications and reminders

## Setup Instructions

1. Create a Firebase project and download the service account key
2. Rename the downloaded key to `firebase-credentials.json` and place it in the project root
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a .env file with the following variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
   ```
5. Run the application:
   ```bash
   flask run
   ```

## API Documentation

### Authentication
- POST /api/auth/login
- POST /api/auth/register

### Events
- GET /api/events
- POST /api/events
- GET /api/events/<event_id>
- PUT /api/events/<event_id>
- DELETE /api/events/<event_id>

### Users
- GET /api/users
- POST /api/users
- GET /api/users/<user_id>
- PUT /api/users/<user_id>
- DELETE /api/users/<user_id>
