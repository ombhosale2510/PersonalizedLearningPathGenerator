import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database
from database import Base, engine

# Import routes
from routes.auth_routes import register_auth_routes
from routes.course_routes import register_course_routes
from routes.learning_path_routes import register_learning_path_routes

# Create and configure the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-for-dev')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-for-dev')

# Set up JWT
jwt = JWTManager(app)

# Set up CORS
CORS(app)

# Set up API
api = Api(app)

# Register routes
register_auth_routes(api)
register_course_routes(api)
register_learning_path_routes(api)

# Create database tables
# Note: We're now creating tables directly when the app is started
# instead of using the deprecated @app.before_first_request
def create_tables():
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == '__main__':
    # Create tables before the app starts
    create_tables()
    app.run(debug=True)