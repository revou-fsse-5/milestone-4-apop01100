from flask import jsonify, request
from app.services.accounts_service import AccountsService
from app.utils.validator import CreateAccountValidator, UpdateAccountValidator
from app.utils.auth import role_required
from app.constant.messages import Messages
from pydantic import ValidationError

class AccountsControllers:
    @staticmethod
    @role_required("user")
    def create_account(payload):
        data = request.json
        data["user_id"] = payload["user_id"]
        
        try:
            account_validated = CreateAccountValidator.model_validate(data)
        except ValidationError as e:
            return jsonify(Messages.error(e)), 400
        
        response = AccountsService.create_account(account_validated.model_dump())
        
        return response
    
    @staticmethod
    @role_required("user", "admin")
    def show_accounts(payload):
        
        if payload["role"] == "user":
            response = AccountsService.show_user_accounts(payload)
            
        if payload["role"] == "admin":
            response = AccountsService.show_all_accounts()
        
        return response
    
    @staticmethod
    @role_required("user")
    def show_account_detail(payload, id):
        response = AccountsService.show_account_detail(payload,id)
        
        return response
    
    @staticmethod
    @role_required("user")
    def account_update(payload, id):
        data = request.json
        
        try:
            account_validator = UpdateAccountValidator.model_validate(data)
        except Exception as e:
            return jsonify(Messages.error(e)), 400
        
        response = AccountsService.account_update(payload, id, account_validator.model_dump())
        
        return response
    
    @staticmethod
    @role_required("user")
    def account_delete(payload, id):
        response = AccountsService.account_delete(payload, id)
        
        return response