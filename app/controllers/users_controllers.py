from flask import request, jsonify
from app.utils.validator import RegisterValidator, LoginValidator, UpdateUserValidator
from pydantic import ValidationError
from app.services.users_service import UsersService
from app.constant.messages import Messages
from flask_jwt_extended import create_access_token
from app.utils.auth import role_required

class UsersController:
    @staticmethod
    def create_user():            
        data = request.json
        data["role"] = "user"
        
        try:
            register_validator = RegisterValidator.model_validate(data)
        except ValidationError as e:
            return jsonify({
                "message": Messages.error(e)
            }), 400
            
        response = UsersService.create_user(register_validator.model_dump())
        
        return response
    
    @staticmethod
    @role_required("super_admin")
    def create_admin(payload):
        data = request.json
        data["role"] = "admin"
        
        try:
            register_validator = RegisterValidator.model_validate(data)
        except ValidationError as e:
            return jsonify(Messages.error(e)), 400
            
        response = UsersService.create_user(register_validator.model_dump())
        
        return response
    
    @staticmethod
    def login_user():
        data = request.json
        
        try:
            login_validator = LoginValidator.model_validate(data)
        except ValidationError as e:
            return jsonify({
                "message": Messages.error(e)
            }), 400
            
        response = UsersService.login_user(login_validator.model_dump())
        
        if "payload" in response:
            payload = response["payload"]
            access_token = create_access_token(identity=payload)
            
            return jsonify({
                "message": response["message"],
                "access_token": access_token
            }), 200
        else:
            return response
            
    @staticmethod
    @role_required("user", "admin", "super_admin")
    def user_profile(payload):
        response =UsersService.user_profile(payload)
        
        return response
    
    @staticmethod
    @role_required("user", "admin", "super_admin")
    def user_update(payload):
        data = request.json
        
        try:
            update_validator = UpdateUserValidator.model_validate(data)
        except ValidationError as e:
            return jsonify(Messages.error(e)), 400
        
        response = UsersService.user_update(payload, update_validator.model_dump())
        
        return response
    
    @staticmethod
    @role_required("admin", "super_admin")
    def show_all_users(payload):
        response = UsersService.show_all_users()
        
        return response
    
    @staticmethod
    @role_required("super_admin")
    def show_all_admin(payload):
        response = UsersService.show_all_admin()
        
        return response
            
        
        
        
        
        
        