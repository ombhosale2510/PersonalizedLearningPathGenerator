from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import SessionLocal
from models.course import Course, CourseTopic, Enrollment, LearningPath, LearningPathItem
from models.user import User
from sqlalchemy.orm import joinedload
from datetime import datetime

class CourseListResource(Resource):
    def get(self):
        db = SessionLocal()
        courses = db.query(Course).all()
        
        results = []
        for course in courses:
            results.append({
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "difficulty": course.difficulty.value if course.difficulty else None,
                "duration_hours": course.duration_hours
            })
        
        db.close()
        return results, 200
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('title'):
            return {"message": "Missing required fields"}, 400
        
        db = SessionLocal()
        
        # Create new course
        new_course = Course(
            title=data['title'],
            description=data.get('description', ''),
            difficulty=data.get('difficulty', 'beginner'),
            duration_hours=data.get('duration_hours', 0)
        )
        
        db.add(new_course)
        db.commit()
        
        # Add topics if provided
        if data.get('topics'):
            for topic_name in data['topics']:
                topic = CourseTopic(
                    course_id=new_course.id,
                    name=topic_name
                )
                db.add(topic)
            
            db.commit()
        
        result = {
            "id": new_course.id,
            "title": new_course.title,
            "description": new_course.description,
            "difficulty": new_course.difficulty.value if new_course.difficulty else None,
            "duration_hours": new_course.duration_hours,
            "created_at": new_course.created_at.isoformat()
        }
        
        db.close()
        return result, 201

class CourseDetailResource(Resource):
    def get(self, course_id):
        db = SessionLocal()
        course = db.query(Course).options(joinedload(Course.topics)).filter(Course.id == course_id).first()
        
        if not course:
            db.close()
            return {"message": "Course not found"}, 404
        
        topics = [topic.name for topic in course.topics]
        
        result = {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "difficulty": course.difficulty.value if course.difficulty else None,
            "duration_hours": course.duration_hours,
            "created_at": course.created_at.isoformat(),
            "topics": topics
        }
        
        db.close()
        return result, 200
    
    @jwt_required()
    def put(self, course_id):
        data = request.get_json()
        
        db = SessionLocal()
        course = db.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            db.close()
            return {"message": "Course not found"}, 404
        
        # Update course fields
        if data.get('title'):
            course.title = data['title']
        if data.get('description') is not None:
            course.description = data['description']
        if data.get('difficulty'):
            course.difficulty = data['difficulty']
        if data.get('duration_hours'):
            course.duration_hours = data['duration_hours']
        
        db.commit()
        
        # Update topics if provided
        if data.get('topics'):
            # Delete existing topics
            db.query(CourseTopic).filter(CourseTopic.course_id == course_id).delete()
            
            # Add new topics
            for topic_name in data['topics']:
                topic = CourseTopic(
                    course_id=course.id,
                    name=topic_name
                )
                db.add(topic)
            
            db.commit()
        
        db.close()
        return {"message": "Course updated successfully"}, 200
    
    @jwt_required()
    def delete(self, course_id):
        db = SessionLocal()
        course = db.query(Course).filter(Course.id == course_id).first()
        
        if not course:
            db.close()
            return {"message": "Course not found"}, 404
        
        # Delete related records
        db.query(CourseTopic).filter(CourseTopic.course_id == course_id).delete()
        db.query(Enrollment).filter(Enrollment.course_id == course_id).delete()
        db.query(LearningPathItem).filter(LearningPathItem.course_id == course_id).delete()
        
        # Delete the course
        db.delete(course)
        db.commit()
        db.close()
        
        return {"message": "Course deleted successfully"}, 200

class EnrollmentResource(Resource):
    @jwt_required()
    def post(self, course_id):
        user_id = get_jwt_identity()
        
        db = SessionLocal()
        
        # Check if course exists
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            db.close()
            return {"message": "Course not found"}, 404
        
        # Check if user is already enrolled
        existing_enrollment = db.query(Enrollment).filter(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id
        ).first()
        
        if existing_enrollment:
            db.close()
            return {"message": "User is already enrolled in this course"}, 409
        
        # Create enrollment
        enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id,
            enrolled_at=datetime.utcnow(),
            progress_percentage=0.0
        )
        
        db.add(enrollment)
        db.commit()
        
        result = {
            "id": enrollment.id,
            "user_id": enrollment.user_id,
            "course_id": enrollment.course_id,
            "enrolled_at": enrollment.enrolled_at.isoformat(),
            "progress_percentage": enrollment.progress_percentage
        }
        
        db.close()
        return result, 201
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        db = SessionLocal()
        enrollments = db.query(Enrollment).options(
            joinedload(Enrollment.course)
        ).filter(Enrollment.user_id == user_id).all()
        
        results = []
        for enrollment in enrollments:
            results.append({
                "enrollment_id": enrollment.id,
                "course_id": enrollment.course_id,
                "course_title": enrollment.course.title,
                "enrolled_at": enrollment.enrolled_at.isoformat(),
                "completed_at": enrollment.completed_at.isoformat() if enrollment.completed_at else None,
                "progress_percentage": enrollment.progress_percentage
            })
        
        db.close()
        return results, 200

def register_course_routes(api):
    api.add_resource(CourseListResource, '/api/courses')
    api.add_resource(CourseDetailResource, '/api/courses/<int:course_id>')
    api.add_resource(EnrollmentResource, '/api/courses/<int:course_id>/enroll', '/api/enrollments')