import pytest
import os
import tempfile
from app import app as flask_app
from database import Base, engine, SessionLocal
from models.user import User
from models.course import Course, CourseTopic, Enrollment, LearningPath, LearningPathItem

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Set up test config
    flask_app.config.update({
        'TESTING': True,
        'JWT_SECRET_KEY': 'test-secret-key',
    })
    
    # Yield the app for testing
    with flask_app.app_context():
        yield flask_app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def db_session():
    """Create a fresh database session for each test."""
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create a session
    session = SessionLocal()
    
    yield session
    
    # Clean up after test
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def auth_headers(client, db_session):
    """Create a user and get auth headers."""
    # Create a test user
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()
    
    # Login and get token
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    token = response.json['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_course(db_session):
    """Create a sample course for testing."""
    course = Course(
        title="Test Course",
        description="A test course for unit tests",
        difficulty="beginner",
        duration_hours=10
    )
    db_session.add(course)
    db_session.commit()
    
    # Add a topic
    topic = CourseTopic(
        course_id=course.id,
        name="Test Topic"
    )
    db_session.add(topic)
    db_session.commit()
    
    return course