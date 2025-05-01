from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class DifficultyLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.BEGINNER)
    duration_hours = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    topics = relationship("CourseTopic", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
    learning_path_items = relationship("LearningPathItem", back_populates="course")

class CourseTopic(Base):
    __tablename__ = 'course_topics'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'))
    name = Column(String(100), nullable=False)
    
    # Relationships
    course = relationship("Course", back_populates="topics")

class Enrollment(Base):
    __tablename__ = 'enrollments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    progress_percentage = Column(Float, default=0.0)
    
    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class LearningPath(Base):
    __tablename__ = 'learning_paths'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="learning_paths")
    items = relationship("LearningPathItem", back_populates="learning_path")

class LearningPathItem(Base):
    __tablename__ = 'learning_path_items'
    
    id = Column(Integer, primary_key=True)
    learning_path_id = Column(Integer, ForeignKey('learning_paths.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    order = Column(Integer, nullable=False)
    
    # Relationships
    learning_path = relationship("LearningPath", back_populates="items")
    course = relationship("Course", back_populates="learning_path_items")