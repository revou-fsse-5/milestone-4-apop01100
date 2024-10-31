from flask import jsonify
from app.connections.db import Session
from app.models.users_model import User
from app.constant.messages import Messages

class UsersService:
    @staticmethod
    def create_user(data):
        with Session() as session:
            try:
                new_user: User = User(
                    username = data["username"],
                    email = data["email"],
                    role=data["role"]
                )
                new_user.set_password(data["password_hash"])
                
                session.add(new_user)
                session.commit()
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400
            
            return jsonify({
                "messages": Messages.CREATE_USER_SUCCESS,
                "new_user_info": new_user.to_dict()
            }), 200
    
    @staticmethod
    def login_user(data):
        username = data["username"]
        password = data["password"]
        
        with Session() as session:
            try:
                user_check: User = session.query(User).filter(User.username == username).first()
                if user_check is None:
                    return jsonify({"message": Messages.USERNAME_NOT_FOUND}), 404
                
                if user_check.check_password(password):
                    payload = {
                        "user_id": user_check.id,
                        "username": user_check.username,
                        "role": user_check.role
                    }
                    
                    return {
                        "message": Messages.LOGIN_SUCCESS,
                        "payload": payload
                    }
                
                else:
                    return jsonify({"message": Messages.INCORRECT_PASSWORD}), 403
            except Exception as e:
                return jsonify(Messages.error(e)), 400
            
    @staticmethod
    def user_profile(payload):
        with Session() as session:
            try:
                user_profile = session.query(User).filter_by(id=payload["user_id"], username=payload["username"]).first()
                accounts_profile = [account.to_dict() for account in user_profile.accounts]
                return jsonify({
                    "user_profile": user_profile.to_dict(),
                    "user_accounts": accounts_profile
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400
    
    @staticmethod
    def user_update(payload, data):
        with Session() as session:
            try:
                user: User = session.query(User).filter_by(id=payload["user_id"], username=payload["username"]).first()
            
                if data["username"] is not None:
                    user.username = data["username"]
                
                if data["email"] is not None:
                    user.email = data["email"]
                
                if data["password"] is not None:
                    user.set_password(data["password"])
                
                session.commit()
                
                return jsonify({
                    "message": Messages.SUCCESS_UPDATE_USER,
                    "user_update": user.to_dict()
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400