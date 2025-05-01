# Frontend Setup and Usage

This document explains how to set up and use the frontend of the Personalized Learning Path Generator.

## Technology Stack

The frontend is built using:
- React with TypeScript for UI components
- React Router for navigation
- Axios for API communication
- Tailwind CSS for styling

## Directory Structure

```
frontend/
  reactapp/
    public/              # Static files
    src/
      components/        # Reusable UI components
      context/           # React context for state management
      pages/             # Page components
      services/          # API services and TypeScript interfaces
      App.tsx            # Main application component
      index.tsx          # Entry point
```

## Initial Setup

### Installing Dependencies

To set up the frontend, navigate to the frontend directory and install the dependencies:

```bash
cd frontend/reactapp
npm install
```

### Tailwind CSS Configuration

The project uses Tailwind CSS for styling. The specific version requirements are:

```bash
npm install -D tailwindcss@3.3.0 postcss@8.4.23 autoprefixer@10.4.14
```

The project includes the following configuration files:

1. **postcss.config.js**:
```javascript
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

2. **tailwind.config.js**:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

3. **src/index.css** (includes the Tailwind directives):
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Additional CSS rules */
```

## Running the Frontend

To start the development server:

```bash
cd frontend/reactapp
npm start
```

The application will be available at http://localhost:3000

## Key Features

1. **Authentication**
   - User registration and login via the LoginPage and RegisterPage components
   - Protected routes for authenticated users using the AuthContext
   - JWT token-based authentication with the backend

2. **Course Management**
   - Browse available courses on the CoursesPage
   - View course details
   - Enroll in courses (for authenticated users)

3. **Learning Path Generation**
   - Create personalized learning paths based on interests using the LearningPathsPage
   - Select difficulty level (Beginner, Intermediate, Advanced)
   - Browse and manage existing learning paths

## Authentication Context

The application uses React Context API to manage authentication state across the application:

- **AuthContext.tsx**: Provides authentication state and methods to login, logout, and register
- Authentication state includes:
  - isAuthenticated: boolean
  - user: User object (when authenticated)
  - token: JWT token for API requests
  - isLoading: loading state during authentication operations

The AuthContext ensures that:
- Protected routes are only accessible to authenticated users
- The Navbar displays different options based on authentication state
- API requests include authentication tokens when needed

## API Communication

The frontend communicates with the backend API using services defined in `src/services/api.ts`. 
All API endpoints are accessed through these service functions, which handle:

- Authentication with JWT tokens
- Data fetching and sending
- Error handling

## Frontend-Backend Integration

The frontend expects the backend API to be running at `http://localhost:5000`. If you change the port or host of your backend, update the `API_URL` constant in `src/services/api.ts`.

## Troubleshooting

### Tailwind CSS Issues

If you encounter issues with Tailwind CSS:

1. **Check Versions**:
   Make sure you have the compatible versions installed:
   ```bash
   npm list tailwindcss postcss autoprefixer
   ```

2. **Configuration Files**:
   Verify that the tailwind.config.js and postcss.config.js files exist and have the correct content

3. **CSS Directives**:
   Ensure index.css includes the necessary Tailwind directives (@tailwind base, components, utilities)

4. **Rebuild Node Modules**:
   If issues persist, try:
   ```bash
   rm -rf node_modules
   npm install
   ```

### React Router Issues

If you encounter issues with routing:

1. Ensure you're using BrowserRouter at the root of your app
2. Check that all route paths are correctly defined in App.tsx
3. Verify that protected routes are properly wrapped with the authentication check

## Adding New Features

When adding new features to the frontend:

1. Create new TypeScript interfaces in `services/types.ts` if needed
2. Add API service functions in `services/api.ts`
3. Create new React components in the appropriate directories
4. Update routing in App.tsx if adding new pages