# API Documentation

This document provides details about the RESTful API endpoints available in the Personalized Learning Path Generator application.

## Base URL

All endpoints are relative to the base URL:

```
http://localhost:5000
```

## Authentication

Most endpoints require authentication using JSON Web Tokens (JWT). To authenticate:

1. Register or login to get an access token
2. Include the token in the Authorization header for subsequent requests:

```
Authorization: Bearer <your_access_token>
```

## API Endpoints

### Authentication Endpoints

#### Register a New User

- **URL**: `/api/auth/register`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
  ```json
  {
    "username": "username",
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "message": "User registered successfully",
    "access_token": "jwt_token_here",
    "user": {
      "id": 1,
      "username": "username",
      "email": "user@example.com"
    }
  }
  ```

#### Login

- **URL**: `/api/auth/login`
- **Method**: `POST`
- **Auth Required**: No
- **Request Body**:
  ```json
  {
    "username": "username",
    "password": "password123"
  }
  ```
  OR
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Login successful",
    "access_token": "jwt_token_here",
    "user": {
      "id": 1,
      "username": "username",
      "email": "user@example.com"
    }
  }
  ```

#### Get User Profile

- **URL**: `/api/auth/profile`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "username": "username",
    "email": "user@example.com",
    "created_at": "2025-05-01T12:00:00"
  }
  ```

### Course Endpoints

#### List All Courses

- **URL**: `/api/courses`
- **Method**: `GET`
- **Auth Required**: No
- **Success Response**: `200 OK`
  ```json
  [
    {
      "id": 1,
      "title": "Introduction to Python",
      "description": "Learn Python basics",
      "difficulty": "beginner",
      "duration_hours": 10
    },
    {
      "id": 2,
      "title": "Advanced JavaScript",
      "description": "Master JavaScript concepts",
      "difficulty": "advanced",
      "duration_hours": 15
    }
  ]
  ```

#### Create a Course

- **URL**: `/api/courses`
- **Method**: `POST`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "title": "Introduction to Python",
    "description": "Learn Python basics",
    "difficulty": "beginner",
    "duration_hours": 10,
    "topics": ["Python", "Programming"]
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": 1,
    "title": "Introduction to Python",
    "description": "Learn Python basics",
    "difficulty": "beginner",
    "duration_hours": 10,
    "created_at": "2025-05-01T12:00:00"
  }
  ```

#### Get Course Details

- **URL**: `/api/courses/{course_id}`
- **Method**: `GET`
- **Auth Required**: No
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "title": "Introduction to Python",
    "description": "Learn Python basics",
    "difficulty": "beginner",
    "duration_hours": 10,
    "created_at": "2025-05-01T12:00:00",
    "topics": ["Python", "Programming"]
  }
  ```

#### Update a Course

- **URL**: `/api/courses/{course_id}`
- **Method**: `PUT`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "title": "Updated Python Course",
    "description": "Updated description",
    "difficulty": "intermediate",
    "duration_hours": 12,
    "topics": ["Python", "Programming", "Data Science"]
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Course updated successfully"
  }
  ```

#### Delete a Course

- **URL**: `/api/courses/{course_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Course deleted successfully"
  }
  ```

#### Enroll in a Course

- **URL**: `/api/courses/{course_id}/enroll`
- **Method**: `POST`
- **Auth Required**: Yes
- **Success Response**: `201 Created`
  ```json
  {
    "id": 1,
    "user_id": 1,
    "course_id": 1,
    "enrolled_at": "2025-05-01T12:00:00",
    "progress_percentage": 0
  }
  ```

#### List User Enrollments

- **URL**: `/api/enrollments`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
  ```json
  [
    {
      "enrollment_id": 1,
      "course_id": 1,
      "course_title": "Introduction to Python",
      "enrolled_at": "2025-05-01T12:00:00",
      "completed_at": null,
      "progress_percentage": 0
    }
  ]
  ```

### Learning Path Endpoints

#### List User's Learning Paths

- **URL**: `/api/learning-paths`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
  ```json
  [
    {
      "id": 1,
      "title": "Web Development Path",
      "description": "Learning path for web development",
      "created_at": "2025-05-01T12:00:00"
    }
  ]
  ```

#### Create a Learning Path

- **URL**: `/api/learning-paths`
- **Method**: `POST`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "title": "Web Development Path",
    "description": "Learning path for web development",
    "course_ids": [1, 2, 3]
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": 1,
    "user_id": 1,
    "title": "Web Development Path",
    "description": "Learning path for web development",
    "created_at": "2025-05-01T12:00:00",
    "courses": [
      {
        "order": 1,
        "course_id": 1,
        "course_title": "Introduction to HTML"
      },
      {
        "order": 2,
        "course_id": 2,
        "course_title": "CSS Fundamentals"
      },
      {
        "order": 3,
        "course_id": 3,
        "course_title": "JavaScript Basics"
      }
    ]
  }
  ```

#### Get Learning Path Details

- **URL**: `/api/learning-paths/{path_id}`
- **Method**: `GET`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
  ```json
  {
    "id": 1,
    "user_id": 1,
    "title": "Web Development Path",
    "description": "Learning path for web development",
    "created_at": "2025-05-01T12:00:00",
    "courses": [
      {
        "order": 1,
        "course_id": 1,
        "course_title": "Introduction to HTML",
        "difficulty": "beginner",
        "duration_hours": 5
      },
      {
        "order": 2,
        "course_id": 2,
        "course_title": "CSS Fundamentals",
        "difficulty": "beginner",
        "duration_hours": 8
      },
      {
        "order": 3,
        "course_id": 3,
        "course_title": "JavaScript Basics",
        "difficulty": "intermediate",
        "duration_hours": 10
      }
    ]
  }
  ```

#### Update a Learning Path

- **URL**: `/api/learning-paths/{path_id}`
- **Method**: `PUT`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "title": "Updated Web Development Path",
    "description": "Updated learning path",
    "course_ids": [1, 3, 4]
  }
  ```
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Learning path updated successfully"
  }
  ```

#### Delete a Learning Path

- **URL**: `/api/learning-paths/{path_id}`
- **Method**: `DELETE`
- **Auth Required**: Yes
- **Success Response**: `200 OK`
  ```json
  {
    "message": "Learning path deleted successfully"
  }
  ```

#### Generate Personalized Learning Path

- **URL**: `/api/learning-paths/generate`
- **Method**: `POST`
- **Auth Required**: Yes
- **Request Body**:
  ```json
  {
    "title": "My Python Journey",
    "description": "Personalized path for Python",
    "interests": ["Python", "Web Development", "Data Science"],
    "difficulty_level": "beginner",
    "max_courses": 5
  }
  ```
- **Success Response**: `201 Created`
  ```json
  {
    "id": 2,
    "user_id": 1,
    "title": "My Python Journey",
    "description": "Personalized path for Python",
    "created_at": "2025-05-01T12:00:00",
    "courses": [
      {
        "order": 1,
        "course_id": 1,
        "course_title": "Introduction to Python"
      },
      {
        "order": 2,
        "course_id": 4,
        "course_title": "Python Web Development with Flask"
      },
      {
        "order": 3,
        "course_id": 5,
        "course_title": "Data Science with Python"
      }
    ]
  }
  ```

## Error Responses

All endpoints may return the following error responses:

- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Missing or invalid authentication token
- **404 Not Found**: Resource not found
- **409 Conflict**: Resource already exists or conflict with existing data
- **500 Internal Server Error**: Server error