from flask import jsonify, request
from app.services.transactions_service import TransactionsService
from app.utils.auth import role_required
from app.utils.validator import CreateTransactionValidator
from pydantic import ValidationError
from app.constant.messages import Messages

class TransactionControllers:
    @staticmethod
    @role_required("user", "admin")
    def show_all_transaction(payload):
        response = TransactionsService.show_transactions(payload)
        
        return response
    
    @staticmethod
    @role_required("user", "admin")
    def transaction_detail(payload, id):
        response = TransactionsService.transaction_detail(payload, id)
        
        return response
    
    @staticmethod
    @role_required("user")
    def create_transaction(payload):
        data = request.json
        
        try:
            transaction_validator = CreateTransactionValidator.model_validate(data)
        except ValidationError as e:
            return jsonify(Messages.error(e))
        
        if data["transaction_type"] == "transfer":
            response = TransactionsService.transfer_transaction(payload, transaction_validator.model_dump())
            
        if data["transaction_type"] == "withdrawal":
            response = TransactionsService.withdrawal_transaction(payload, transaction_validator.model_dump())
            
        if data["transaction_type"] == "deposit":
            response = TransactionsService.deposit_transaction(payload, transaction_validator.model_dump())
        
        return response