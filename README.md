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

### Base URL
All API endpoints are prefixed with: `http://localhost:5000/api`

### Authentication
Most endpoints require authentication via JWT token. Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

### API Endpoints

### Authentication

#### Register User
- **URL**: `/auth/register`
- **Method**: `POST`
- **Auth Required**: No
- **Body**:
```json
{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe",
    "role": "worker"  // or "manager"
}
```
- **Success Response**: `201 Created`
```json
{
    "message": "User created successfully",
    "user_id": "user_id_here"
}
```

#### Login
- **URL**: `/auth/login`
- **Method**: `POST`
- **Auth Required**: No
- **Body**:
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```
- **Success Response**: `200 OK`
```json
{
    "token": "jwt_token_here",
    "user": {
        "id": "user_id",
        "email": "user@example.com",
        "name": "John Doe",
        "role": "worker"
    }
}
```

### Events

#### Get All Events
- **URL**: `/events/`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
[
    {
        "id": "event_id",
        "title": "Event Title",
        "description": "Event Description",
        "date": "2025-02-01T14:00:00Z",
        "capacity": 10,
        "registered_workers": []
    }
]
```

#### Create Event
- **URL**: `/events/`
- **Method**: `POST`
- **Auth Required**: Yes (Manager only)
- **Body**:
```json
{
    "title": "Event Title",
    "description": "Event Description",
    "date": "2025-02-01T14:00:00Z",
    "capacity": 10
}
```
- **Success Response**: `201 Created`
```json
{
    "message": "Event created successfully",
    "event_id": "event_id_here"
}
```

#### Get Event by ID
- **URL**: `/events/<event_id>`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
{
    "id": "event_id",
    "title": "Event Title",
    "description": "Event Description",
    "date": "2025-02-01T14:00:00Z",
    "capacity": 10,
    "registered_workers": []
}
```

#### Update Event
- **URL**: `/events/<event_id>`
- **Method**: `PUT`
- **Auth Required**: Yes (Manager only)
- **Body**: Same as Create Event
- **Success Response**: `200 OK`
```json
{
    "message": "Event updated successfully"
}
```

#### Delete Event
- **URL**: `/events/<event_id>`
- **Method**: `DELETE`
- **Auth Required**: Yes (Manager only)
- **Success Response**: `200 OK`
```json
{
    "message": "Event deleted successfully"
}
```

#### Register for Event
- **URL**: `/events/<event_id>/register`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
{
    "message": "Successfully registered for event"
}
```

#### Unregister from Event
- **URL**: `/events/<event_id>/unregister`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
```json
{
    "message": "Successfully unregistered from event"
}
```

### Users

#### Get All Users
- **URL**: `/users/`
- **Method**: `GET`
- **Auth Required**: Yes (Manager only)
- **Success Response**: `200 OK`
```json
[
    {
        "id": "user_id",
        "email": "user@example.com",
        "name": "John Doe",
        "role": "worker"
    }
]
```

#### Get User by ID
- **URL**: `/users/<user_id>`
- **Method**: `GET`
- **Auth Required**: Yes (Manager or same user)
- **Success Response**: `200 OK`
```json
{
    "id": "user_id",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "worker"
}
```

#### Update User
- **URL**: `/users/<user_id>`
- **Method**: `PUT`
- **Auth Required**: Yes (Manager or same user)
- **Body**:
```json
{
    "name": "Updated Name",
    "email": "updated@example.com"
}
```
- **Success Response**: `200 OK`
```json
{
    "message": "User updated successfully"
}
```

#### Delete User
- **URL**: `/users/<user_id>`
- **Method**: `DELETE`
- **Auth Required**: Yes (Manager only)
- **Success Response**: `200 OK`
```json
{
    "message": "User deleted successfully"
}
```

## Error Responses
All endpoints may return the following errors:

- `400 Bad Request`: When required fields are missing or invalid
- `401 Unauthorized`: When authentication fails or token is missing
- `403 Forbidden`: When user doesn't have required permissions
- `404 Not Found`: When requested resource doesn't exist
- `500 Internal Server Error`: When server encounters an error

## Rate Limiting
- API calls are limited to 100 requests per minute per IP address
- Exceeding this limit will result in a `429 Too Many Requests` response

## Testing
To run the test suite:
```bash
cd backend/tests
python test_server.py
