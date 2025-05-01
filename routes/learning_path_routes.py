from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import SessionLocal
from models.course import LearningPath, LearningPathItem
from models.user import User
from sqlalchemy.orm import joinedload
from services.learning_path_service import LearningPathService

class LearningPathListResource(Resource):
    @jwt_required()
    def get(self):
        """Get all learning paths for the current user"""
        user_id = get_jwt_identity()
        
        db = SessionLocal()
        learning_paths = db.query(LearningPath).filter(LearningPath.user_id == user_id).all()
        
        results = []
        for path in learning_paths:
            results.append({
                "id": path.id,
                "title": path.title,
                "description": path.description,
                "created_at": path.created_at.isoformat()
            })
        
        db.close()
        return results, 200
    
    @jwt_required()
    def post(self):
        """Create a new learning path"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('title'):
            return {"message": "Missing required fields"}, 400
        
        result, error = LearningPathService.create_learning_path(
            user_id=user_id,
            title=data['title'],
            description=data.get('description', ''),
            course_ids=data.get('course_ids', [])
        )
        
        if error:
            return {"message": error}, 400
            
        return result, 201

class LearningPathDetailResource(Resource):
    @jwt_required()
    def get(self, path_id):
        """Get a specific learning path by ID"""
        user_id = get_jwt_identity()
        
        db = SessionLocal()
        learning_path = db.query(LearningPath).options(
            joinedload(LearningPath.items).joinedload(LearningPathItem.course)
        ).filter(LearningPath.id == path_id, LearningPath.user_id == user_id).first()
        
        if not learning_path:
            db.close()
            return {"message": "Learning path not found"}, 404
        
        # Format courses in the learning path
        courses = []
        for item in sorted(learning_path.items, key=lambda x: x.order):
            courses.append({
                "order": item.order,
                "course_id": item.course_id,
                "course_title": item.course.title,
                "difficulty": item.course.difficulty.value if item.course.difficulty else None,
                "duration_hours": item.course.duration_hours
            })
        
        result = {
            "id": learning_path.id,
            "user_id": learning_path.user_id,
            "title": learning_path.title,
            "description": learning_path.description,
            "created_at": learning_path.created_at.isoformat(),
            "courses": courses
        }
        
        db.close()
        return result, 200
    
    @jwt_required()
    def put(self, path_id):
        """Update a learning path"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        db = SessionLocal()
        learning_path = db.query(LearningPath).filter(
            LearningPath.id == path_id, 
            LearningPath.user_id == user_id
        ).first()
        
        if not learning_path:
            db.close()
            return {"message": "Learning path not found"}, 404
        
        # Update basic information
        if data.get('title'):
            learning_path.title = data['title']
        if data.get('description') is not None:
            learning_path.description = data['description']
        
        db.commit()
        
        # Update courses if provided
        if data.get('course_ids'):
            # Remove existing items
            db.query(LearningPathItem).filter(LearningPathItem.learning_path_id == path_id).delete()
            
            # Add new items
            for index, course_id in enumerate(data['course_ids']):
                path_item = LearningPathItem(
                    learning_path_id=path_id,
                    course_id=course_id,
                    order=index + 1
                )
                db.add(path_item)
            
            db.commit()
        
        db.close()
        return {"message": "Learning path updated successfully"}, 200
    
    @jwt_required()
    def delete(self, path_id):
        """Delete a learning path"""
        user_id = get_jwt_identity()
        
        db = SessionLocal()
        learning_path = db.query(LearningPath).filter(
            LearningPath.id == path_id, 
            LearningPath.user_id == user_id
        ).first()
        
        if not learning_path:
            db.close()
            return {"message": "Learning path not found"}, 404
        
        # Delete related records
        db.query(LearningPathItem).filter(LearningPathItem.learning_path_id == path_id).delete()
        
        # Delete the learning path
        db.delete(learning_path)
        db.commit()
        db.close()
        
        return {"message": "Learning path deleted successfully"}, 200

class GeneratePathResource(Resource):
    @jwt_required()
    def post(self):
        """Generate a personalized learning path based on interests and preferences"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('title') or not data.get('interests'):
            return {"message": "Missing required fields"}, 400
        
        # Generate recommended course IDs
        recommended_course_ids = LearningPathService.generate_personalized_path(
            user_id=user_id,
            interests=data['interests'],
            difficulty_level=data.get('difficulty_level'),
            max_courses=data.get('max_courses', 5)
        )
        
        # Create learning path with recommended courses
        result, error = LearningPathService.create_learning_path(
            user_id=user_id,
            title=data['title'],
            description=data.get('description', 'Generated learning path'),
            course_ids=recommended_course_ids
        )
        
        if error:
            return {"message": error}, 400
            
        return result, 201

def register_learning_path_routes(api):
    api.add_resource(LearningPathListResource, '/api/learning-paths')
    api.add_resource(LearningPathDetailResource, '/api/learning-paths/<int:path_id>')
    api.add_resource(GeneratePathResource, '/api/learning-paths/generate')