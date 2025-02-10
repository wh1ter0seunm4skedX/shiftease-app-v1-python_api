# ShiftEase Backend

The backend service for ShiftEase, built with Flask and Firebase.

## Technology Stack

- **Framework**: Flask
- **Database**: Firebase Firestore
- **Authentication**: JWT + Firebase Auth
- **Testing**: Python unittest
- **Documentation**: OpenAPI/Swagger

## Project Structure

```
backend/
├── app/
│   ├── models/        # Data models
│   ├── routes/        # API endpoints
│   ├── services/      # Business logic
│   └── __init__.py    # App initialization
├── config/
│   └── config.py      # Configuration settings
├── scripts/           # Utility scripts
├── tests/             # Test suite
├── .env.example       # Environment variables template
├── requirements.txt   # Python dependencies
└── run.py            # Application entry point
```

## Setup Instructions

1. Create a Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Firebase:
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Go to Project Settings > Service Accounts
   - Generate a new private key
   - Save the JSON file as `firebase-credentials.json` in the `config/` directory

4. Configure environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
FLASK_APP=run.py
FLASK_ENV=development
FIREBASE_CREDENTIALS_PATH=config/firebase-credentials.json
JWT_SECRET=your-secret-key
TESTING=false
```

5. Run the application:
```bash
python run.py
```

## API Documentation

### Authentication Endpoints

#### POST /api/auth/register
Register a new user
- Body: `{ "email": "string", "password": "string", "name": "string", "role": "string" }`
- Response: `{ "message": "string", "token": "string", "user": {...} }`

#### POST /api/auth/login
Login existing user
- Body: `{ "email": "string", "password": "string" }`
- Response: `{ "token": "string", "user": {...} }`

### Event Endpoints

#### GET /api/events
Get all events
- Auth: Required
- Response: `[{ "id": "string", "title": "string", ... }]`

#### POST /api/events
Create new event
- Auth: Required (Admin only)
- Body: `{ "title": "string", "description": "string", "date": "string", "capacity": "number" }`
- Response: `{ "message": "string", "event": {...} }`

#### PUT /api/events/{id}
Update event
- Auth: Required (Admin only)
- Body: `{ "title": "string", "description": "string", ... }`
- Response: `{ "message": "string", "event": {...} }`

#### DELETE /api/events/{id}
Delete event
- Auth: Required (Admin only)
- Response: `{ "message": "string" }`

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Testing

Run the test suite:
```bash
python -m pytest
```

## Development Guidelines

1. Follow PEP 8 style guide
2. Write unit tests for new features
3. Update documentation for API changes
4. Use meaningful commit messages
5. Create feature branches for new development

## Deployment

1. Set environment variables for production
2. Configure CORS settings for production domain
3. Set up logging and monitoring
4. Configure rate limiting
5. Enable HTTPS

## Troubleshooting

Common issues and solutions:

1. **Firebase Connection Issues**
   - Check credentials file path
   - Verify project configuration
   - Check Firebase Console permissions

2. **Authentication Errors**
   - Verify JWT secret key
   - Check token expiration
   - Confirm user permissions

3. **Database Operations**
   - Check Firestore rules
   - Verify data structure
   - Check connection status
