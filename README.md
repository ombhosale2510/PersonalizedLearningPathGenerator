# Personalized Learning Path Generator

A full-stack application that generates personalized learning paths for users based on their interests, skill levels, and learning goals.

## Project Overview

This application allows users to:
- Register and authenticate
- Browse available courses
- Enroll in courses
- Create custom learning paths
- Generate personalized learning paths based on interests and preferences

## Technology Stack

- **Backend**: Flask (Python) with RESTful API
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Frontend**: React with TypeScript and Tailwind CSS
- **Containerization**: Docker (planned)
- **CI/CD**: Continuous Integration/Deployment (planned)
- **ML/AI**: Machine Learning for personalized recommendations (planned)

## Project Structure

```
├── app.py                  # Main backend application entry point
├── database.py             # Database configuration
├── models/                 # Database models
│   ├── course.py           # Course, Enrollment, and LearningPath models
│   └── user.py             # User model
├── routes/                 # API routes
│   ├── auth_routes.py      # Authentication endpoints
│   ├── course_routes.py    # Course management endpoints
│   └── learning_path_routes.py # Learning path endpoints
├── services/               # Business logic
│   └── learning_path_service.py # Learning path generation
├── tests/                  # Unit tests
│   ├── conftest.py         # Test configuration and fixtures
│   ├── test_auth.py        # Tests for authentication endpoints
│   ├── test_courses.py     # Tests for course management
│   └── test_learning_paths.py # Tests for learning paths
├── frontend/               # React frontend
│   └── reactapp/           # React application
│       ├── public/         # Static files
│       └── src/            # React source code
│           ├── components/ # Reusable UI components
│           ├── context/    # React context (state management)
│           ├── pages/      # Page components
│           └── services/   # API services and TypeScript interfaces
└── docs/                   # Documentation
    ├── api.md              # API documentation
    ├── database.md         # Database setup and management
    ├── frontend.md         # Frontend setup and usage
    ├── roadmap.md          # Development roadmap
    ├── setup.md            # Setup instructions
    └── testing.md          # Testing guide
```

## Getting Started

### Backend Setup

See [setup.md](docs/setup.md) for detailed installation and setup instructions.

### Database Setup

See [database.md](docs/database.md) for PostgreSQL and pgAdmin setup instructions.

### Frontend Setup

See [frontend.md](docs/frontend.md) for React frontend setup and usage instructions.

## Running the Application

### Backend

```bash
# Activate your virtual environment (if using one)
python app.py
```

The backend will run on http://localhost:5000

### Frontend

```bash
cd frontend/reactapp
npm start
```

The frontend will run on http://localhost:3000

## API Documentation

See [api.md](docs/api.md) for detailed API documentation.

## Testing

See [testing.md](docs/testing.md) for information on running tests.

## Development Roadmap

See [roadmap.md](docs/roadmap.md) for the development plan and future enhancements.