# Setup and Installation Guide

This guide will walk you through setting up the Personalized Learning Path Generator application.

## Prerequisites

- Python 3.8+ installed
- PostgreSQL database server installed and running
- Node.js and npm installed (for the React frontend)
- pgAdmin (for database management)

## Backend Setup

1. **Clone the repository**

   If you haven't already cloned the repository, do so now.

2. **Install required Python packages**

   ```bash
   pip install flask flask-restful flask-jwt-extended flask-sqlalchemy flask-cors python-dotenv bcrypt psycopg2-binary
   ```

3. **Set up the PostgreSQL database**

   Create a new PostgreSQL database for the application:

   ```bash
   # Using psql command line tool
   psql -U postgres
   CREATE DATABASE personalized_learning_path;
   ```

   Alternatively, use pgAdmin as described in the [database documentation](database.md).

4. **Configure database connection**

   Update the database connection string in `database.py` with your PostgreSQL credentials:

   ```python
   DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/personalized_learning_path"
   ```

5. **Set up environment variables**

   Create a `.env` file in the project root with the following contents:

   ```
   SECRET_KEY=your-secret-key-for-production
   JWT_SECRET_KEY=your-jwt-secret-for-production
   ```

   Replace the values with secure random strings.

## Frontend Setup

1. **Navigate to the React app directory**

   ```bash
   cd frontend/reactapp
   ```

2. **Install dependencies**

   ```bash
   npm install
   ```

3. **Install Tailwind CSS and its dependencies**

   The frontend uses Tailwind CSS for styling. Install the specific versions that are compatible:

   ```bash
   npm install -D tailwindcss@3.3.0 postcss@8.4.23 autoprefixer@10.4.14
   ```

   Note: The frontend already includes the necessary configuration files for Tailwind CSS (postcss.config.js and tailwind.config.js).

## Running the Application

### Backend

To start the Flask API server:

```bash
python app.py
```

The API server will start on http://127.0.0.1:5000/

### Frontend

To start the React development server:

```bash
cd frontend/reactapp
npm start
```

The frontend will be available at http://localhost:3000

## Database Initialization

The database tables will be automatically created when you run the backend application. The `create_tables()` function in `app.py` handles this during startup.

After the tables are created, you'll need to populate them with initial data. See the [database documentation](database.md) for SQL scripts to add sample courses and users.

## Testing the API

You can test the API using tools like:
- [Postman](https://www.postman.com/downloads/)
- [Insomnia](https://insomnia.rest/download)
- curl commands from the terminal

See the [API documentation](api.md) for examples of how to interact with the endpoints.

## Additional Resources

- [Frontend Documentation](frontend.md): Detailed information about the React frontend
- [Database Documentation](database.md): PostgreSQL and pgAdmin setup and usage
- [API Documentation](api.md): API endpoints and usage examples