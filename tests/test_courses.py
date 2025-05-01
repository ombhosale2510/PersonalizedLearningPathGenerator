import json
import pytest

def test_get_courses(client):
    """Test getting list of courses."""
    response = client.get('/api/courses')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_create_course(client, auth_headers):
    """Test creating a new course."""
    response = client.post('/api/courses', 
        headers=auth_headers,
        json={
            'title': 'New Course',
            'description': 'A brand new course',
            'difficulty': 'intermediate',
            'duration_hours': 15,
            'topics': ['Python', 'Web Development']
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'New Course'
    assert data['description'] == 'A brand new course'
    assert data['difficulty'] == 'intermediate'
    assert data['duration_hours'] == 15
    assert 'created_at' in data

def test_create_course_unauthorized(client):
    """Test creating a course without authentication."""
    response = client.post('/api/courses', 
        json={
            'title': 'New Course',
            'description': 'A brand new course',
            'difficulty': 'intermediate',
            'duration_hours': 15
        }
    )
    
    assert response.status_code == 401

def test_get_course_details(client, sample_course):
    """Test getting course details."""
    response = client.get(f'/api/courses/{sample_course.id}')
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == sample_course.id
    assert data['title'] == sample_course.title
    assert data['description'] == sample_course.description
    assert 'topics' in data
    assert len(data['topics']) == 1
    assert data['topics'][0] == 'Test Topic'

def test_get_nonexistent_course(client):
    """Test getting a course that doesn't exist."""
    response = client.get('/api/courses/9999')
    
    assert response.status_code == 404

def test_update_course(client, auth_headers, sample_course):
    """Test updating a course."""
    response = client.put(
        f'/api/courses/{sample_course.id}',
        headers=auth_headers,
        json={
            'title': 'Updated Course Title',
            'description': 'Updated description',
            'topics': ['Updated Topic', 'New Topic']
        }
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Course updated successfully'
    
    # Verify the update with a GET request
    response = client.get(f'/api/courses/{sample_course.id}')
    data = json.loads(response.data)
    assert data['title'] == 'Updated Course Title'
    assert data['description'] == 'Updated description'
    assert len(data['topics']) == 2
    assert 'Updated Topic' in data['topics']
    assert 'New Topic' in data['topics']

def test_delete_course(client, auth_headers, sample_course):
    """Test deleting a course."""
    response = client.delete(
        f'/api/courses/{sample_course.id}',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Course deleted successfully'
    
    # Verify the course is gone
    response = client.get(f'/api/courses/{sample_course.id}')
    assert response.status_code == 404

def test_enroll_in_course(client, auth_headers, sample_course):
    """Test enrolling in a course."""
    response = client.post(
        f'/api/courses/{sample_course.id}/enroll',
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['course_id'] == sample_course.id
    assert 'user_id' in data
    assert 'enrolled_at' in data
    assert data['progress_percentage'] == 0.0

def test_get_enrollments(client, auth_headers, sample_course):
    """Test getting all enrollments for a user."""
    # First, enroll in the course
    client.post(
        f'/api/courses/{sample_course.id}/enroll',
        headers=auth_headers
    )
    
    # Then get enrollments
    response = client.get('/api/enrollments', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['course_id'] == sample_course.id
    assert data[0]['course_title'] == sample_course.title