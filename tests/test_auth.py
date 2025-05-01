import json
import pytest

def test_register_user(client, db_session):
    """Test user registration endpoint."""
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['username'] == 'newuser'
    assert data['user']['email'] == 'newuser@example.com'

def test_register_duplicate_user(client, db_session, auth_headers):
    """Test registering a user with existing username or email."""
    # Try to register with same username
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'different@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 409
    
    # Try to register with same email
    response = client.post('/api/auth/register', json={
        'username': 'different',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 409

def test_login_success(client, db_session, auth_headers):
    """Test successful login."""
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['username'] == 'testuser'

def test_login_with_email(client, db_session, auth_headers):
    """Test login with email instead of username."""
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert data['user']['email'] == 'test@example.com'

def test_login_invalid_credentials(client, db_session, auth_headers):
    """Test login with invalid credentials."""
    # Wrong password
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    
    # Non-existent user
    response = client.post('/api/auth/login', json={
        'username': 'nonexistentuser',
        'password': 'password123'
    })
    
    assert response.status_code == 401

def test_get_profile(client, auth_headers):
    """Test getting user profile."""
    response = client.get('/api/auth/profile', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'

def test_profile_unauthorized(client):
    """Test accessing profile without authentication."""
    response = client.get('/api/auth/profile')
    
    assert response.status_code == 401