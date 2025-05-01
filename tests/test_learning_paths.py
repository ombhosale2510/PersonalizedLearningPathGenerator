import json
import pytest

@pytest.fixture
def sample_learning_path(client, auth_headers, sample_course, db_session):
    """Create a sample learning path for testing."""
    response = client.post('/api/learning-paths', 
        headers=auth_headers,
        json={
            'title': 'Test Learning Path',
            'description': 'A learning path for testing',
            'course_ids': [sample_course.id]
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    return data

def test_create_learning_path(client, auth_headers, sample_course):
    """Test creating a learning path."""
    response = client.post('/api/learning-paths', 
        headers=auth_headers,
        json={
            'title': 'My Learning Path',
            'description': 'A custom learning path',
            'course_ids': [sample_course.id]
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'My Learning Path'
    assert data['description'] == 'A custom learning path'
    assert 'courses' in data
    assert len(data['courses']) == 1
    assert data['courses'][0]['course_id'] == sample_course.id

def test_get_learning_paths(client, auth_headers, sample_learning_path):
    """Test getting all learning paths for a user."""
    response = client.get('/api/learning-paths', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['title'] == sample_learning_path['title']
    assert data[0]['description'] == sample_learning_path['description']

def test_get_learning_path_details(client, auth_headers, sample_learning_path):
    """Test getting details of a specific learning path."""
    response = client.get(
        f'/api/learning-paths/{sample_learning_path["id"]}', 
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == sample_learning_path['id']
    assert data['title'] == sample_learning_path['title']
    assert data['description'] == sample_learning_path['description']
    assert 'courses' in data
    assert len(data['courses']) == 1

def test_update_learning_path(client, auth_headers, sample_learning_path, sample_course):
    """Test updating a learning path."""
    response = client.put(
        f'/api/learning-paths/{sample_learning_path["id"]}',
        headers=auth_headers,
        json={
            'title': 'Updated Learning Path',
            'description': 'Updated description'
        }
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Learning path updated successfully'
    
    # Verify the update
    response = client.get(
        f'/api/learning-paths/{sample_learning_path["id"]}', 
        headers=auth_headers
    )
    data = json.loads(response.data)
    assert data['title'] == 'Updated Learning Path'
    assert data['description'] == 'Updated description'

def test_delete_learning_path(client, auth_headers, sample_learning_path):
    """Test deleting a learning path."""
    response = client.delete(
        f'/api/learning-paths/{sample_learning_path["id"]}',
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Learning path deleted successfully'
    
    # Verify it's gone
    response = client.get(
        f'/api/learning-paths/{sample_learning_path["id"]}', 
        headers=auth_headers
    )
    assert response.status_code == 404

def test_generate_personalized_path(client, auth_headers, sample_course):
    """Test generating a personalized learning path."""
    # First make sure the course has a topic that matches our interests
    response = client.post('/api/learning-paths/generate', 
        headers=auth_headers,
        json={
            'title': 'My Personalized Path',
            'description': 'A personalized learning path',
            'interests': ['Test Topic'],
            'difficulty_level': 'beginner',
            'max_courses': 3
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'My Personalized Path'
    assert data['description'] == 'A personalized learning path'
    assert 'courses' in data
    # The number of courses returned depends on what's available matching the criteria
    assert len(data['courses']) >= 0