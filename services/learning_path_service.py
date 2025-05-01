from database import SessionLocal
from models.course import Course, LearningPath, LearningPathItem
from models.user import User
from sqlalchemy.orm import joinedload
from datetime import datetime

class LearningPathService:
    @staticmethod
    def create_learning_path(user_id, title, description, course_ids=None):
        """
        Create a new learning path for a user with specified courses
        
        Args:
            user_id: ID of the user creating the learning path
            title: Title of the learning path
            description: Description of the learning path
            course_ids: List of course IDs to add to the learning path (in order)
            
        Returns:
            Dictionary containing the created learning path information
        """
        db = SessionLocal()
        
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            db.close()
            return None, "User not found"
        
        # Create learning path
        learning_path = LearningPath(
            user_id=user_id,
            title=title,
            description=description,
            created_at=datetime.utcnow()
        )
        
        db.add(learning_path)
        db.commit()
        
        # Add courses to learning path if provided
        if course_ids:
            for index, course_id in enumerate(course_ids):
                # Verify course exists
                course = db.query(Course).filter(Course.id == course_id).first()
                if not course:
                    continue
                
                # Add course to learning path
                path_item = LearningPathItem(
                    learning_path_id=learning_path.id,
                    course_id=course_id,
                    order=index + 1
                )
                
                db.add(path_item)
            
            db.commit()
        
        # Get the created learning path with its items
        created_path = db.query(LearningPath).options(
            joinedload(LearningPath.items).joinedload(LearningPathItem.course)
        ).filter(LearningPath.id == learning_path.id).first()
        
        # Format response
        courses = []
        for item in sorted(created_path.items, key=lambda x: x.order):
            courses.append({
                "order": item.order,
                "course_id": item.course_id,
                "course_title": item.course.title
            })
        
        result = {
            "id": created_path.id,
            "user_id": created_path.user_id,
            "title": created_path.title,
            "description": created_path.description,
            "created_at": created_path.created_at.isoformat(),
            "courses": courses
        }
        
        db.close()
        return result, None
    
    @staticmethod
    def generate_personalized_path(user_id, interests, difficulty_level=None, max_courses=5):
        """
        Generate a personalized learning path based on user interests and difficulty level
        
        Args:
            user_id: ID of the user to generate the path for
            interests: List of interest topics
            difficulty_level: Preferred difficulty level (beginner, intermediate, advanced)
            max_courses: Maximum number of courses to include
            
        Returns:
            List of recommended course IDs in suggested order
        """
        db = SessionLocal()
        
        # Start with a query for all courses
        query = db.query(Course).join(Course.topics)
        
        # Filter by interests if provided
        if interests:
            query = query.filter(Course.topics.any(name__in=interests))
        
        # Filter by difficulty if provided
        if difficulty_level:
            query = query.filter(Course.difficulty == difficulty_level)
        
        # Get courses that match criteria, limiting to max_courses
        recommended_courses = query.limit(max_courses).all()
        
        # Get the IDs in the right order (currently just by ID, but could be improved)
        recommended_course_ids = [course.id for course in recommended_courses]
        
        db.close()
        return recommended_course_ids