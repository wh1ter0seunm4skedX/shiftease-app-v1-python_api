# ShiftEase Frontend

The frontend application for ShiftEase, built with React and Material-UI.

## Technology Stack

- **Framework**: React
- **UI Library**: Material-UI (MUI)
- **State Management**: React Context
- **Routing**: React Router
- **HTTP Client**: Axios
- **Authentication**: JWT
- **Form Handling**: React Hook Form
- **Testing**: Jest + React Testing Library

## Project Structure

```
frontend/
├── public/           # Static files
├── src/
│   ├── components/   # Reusable UI components
│   ├── contexts/     # React contexts
│   ├── hooks/        # Custom React hooks
│   ├── pages/        # Page components
│   ├── services/     # API services
│   ├── styles/       # Global styles
│   ├── utils/        # Helper functions
│   └── App.jsx       # Root component
├── .env.example      # Environment variables template
└── package.json      # Dependencies and scripts
```

## Setup Instructions

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
```bash
cp .env.example .env.local
```

Edit `.env.local` with your settings:
```
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=ShiftEase
```

3. Start the development server:
```bash
npm run dev
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run test` - Run tests
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## Features

### User Authentication
- Login/Register forms
- Protected routes
- Role-based access control
- JWT token management

### Event Management
- Event creation and editing
- Event listing and filtering
- Event registration
- Capacity management

### User Interface
- Responsive design
- Dark/Light theme
- Loading states
- Error handling
- Form validation
- Toast notifications

## Development Guidelines

1. Component Structure
   - Use functional components
   - Implement proper prop validation
   - Keep components focused and reusable

2. State Management
   - Use React Context for global state
   - Keep component state minimal
   - Implement proper error boundaries

3. Code Style
   - Follow ESLint configuration
   - Use Prettier for formatting
   - Write meaningful comments
   - Use TypeScript types/interfaces

4. Testing
   - Write unit tests for components
   - Test user interactions
   - Mock API calls
   - Test error scenarios

## Deployment

1. Build the application:
```bash
npm run build
```

2. Configure environment variables for production
3. Set up CI/CD pipeline
4. Configure hosting service
5. Set up monitoring and analytics

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

Common issues and solutions:

1. **API Connection Issues**
   - Check API URL configuration
   - Verify CORS settings
   - Check network requests

2. **Build Problems**
   - Clear npm cache
   - Remove node_modules
   - Check dependency versions

3. **Authentication Issues**
   - Check token storage
   - Verify API endpoints
   - Check token expiration handling
