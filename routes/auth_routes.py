from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import SessionLocal
from models.user import User
import datetime

class RegisterResource(Resource):
    def post(self):
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return {"message": "Missing required fields"}, 400
        
        db = SessionLocal()
        
        # Check if user already exists
        if db.query(User).filter((User.username == data['username']) | (User.email == data['email'])).first():
            db.close()
            return {"message": "User with this username or email already exists"}, 409
        
        # Create new user
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])
        
        db.add(new_user)
        db.commit()
        
        # Create access token
        access_token = create_access_token(
            identity=new_user.id,
            expires_delta=datetime.timedelta(days=1)
        )
        
        db.close()
        
        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            }
        }, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        
        # Validate input
        if not data or not (data.get('username') or data.get('email')) or not data.get('password'):
            return {"message": "Missing required fields"}, 400
        
        db = SessionLocal()
        
        # Find user by username or email
        user = None
        if data.get('username'):
            user = db.query(User).filter(User.username == data['username']).first()
        elif data.get('email'):
            user = db.query(User).filter(User.email == data['email']).first()
            
        if not user or not user.check_password(data['password']):
            db.close()
            return {"message": "Invalid credentials"}, 401
        
        # Create access token
        access_token = create_access_token(
            identity=user.id,
            expires_delta=datetime.timedelta(days=1)
        )
        
        db.close()
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }, 200

class UserProfileResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            db.close()
            return {"message": "User not found"}, 404
        
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        }
        
        db.close()
        return user_data, 200

def register_auth_routes(api):
    api.add_resource(RegisterResource, '/api/auth/register')
    api.add_resource(LoginResource, '/api/auth/login')
    api.add_resource(UserProfileResource, '/api/auth/profile')