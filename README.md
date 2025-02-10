# ShiftEase

A modern event management system designed for volunteer coordination and event organization.

## Overview

ShiftEase is a full-stack web application that helps organizations manage events and coordinate volunteers efficiently. It provides an intuitive interface for both administrators and volunteers to manage event registrations, schedules, and participation.

## Features

- **User Authentication**: Secure login and registration system with role-based access control
- **Event Management**: Create, update, and delete events with detailed information
- **Volunteer Management**: Track volunteer participation and availability
- **Real-time Updates**: Instant notifications for event changes and registrations
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Project Structure

```
ShiftEase/
├── backend/         # Flask backend API
├── frontend/        # React frontend application
├── docs/           # Documentation
└── scripts/        # Utility scripts
```

## Prerequisites

- Node.js (v16 or higher)
- Python (3.8 or higher)
- Firebase account
- Git

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ShiftEase.git
cd ShiftEase
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env     # Configure your environment variables
```

3. Set up the frontend:
```bash
cd frontend
npm install
cp .env.example .env.local  # Configure your environment variables
```

4. Start the development servers:

Backend:
```bash
cd backend
python run.py
```

Frontend:
```bash
cd frontend
npm run dev
```

## Documentation

For detailed setup instructions and API documentation:
- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
