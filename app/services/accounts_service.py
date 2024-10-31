from flask import jsonify
from app.models.accounts_model import Account
from app.connections.db import Session
from app.constant.messages import Messages
from app.utils.functions.generate_account_number import generate_random_account_number 

class AccountsService:
    @staticmethod
    def create_account(data):
        with Session() as session:
            try:
                account_number = generate_random_account_number()
                check_account_number = session.query(Account).filter_by(account_number = account_number).first()
                
                while True:
                    check_account_number = session.query(Account).filter_by(account_number = account_number).first()
                    if check_account_number is None:
                        break
                    
                new_account: Account = Account(
                    user_id=data["user_id"],
                    account_type=data["account_type"],
                    account_number=account_number
                )
                
                session.add(new_account)
                session.commit()
                
                return jsonify({
                    "message": Messages.SUCCESS_CREATE_ACCOUNT
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400
            
    @staticmethod
    def show_user_accounts(payload):
        with Session() as session:
            try:
                accounts = session.query(Account).filter_by(user_id = payload["user_id"], is_deleted = False).all()
                list_accounts = [account.to_dict() for account in accounts]
                
                return jsonify({
                    "accounts": list_accounts
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400
    
    @staticmethod
    def show_all_accounts():
        with Session() as session:
            try:
                accounts = session.query(Account).all()
                list_accounts = [account.to_dict() for account in accounts]
                
                return jsonify({
                    "accounts": list_accounts
                })
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e))
            
    @staticmethod
    def show_account_detail(payload, account_id):
        with Session() as session:
            try:
                account = session.query(Account).filter_by(id = account_id, user_id = payload["user_id"]).first()
                
                if account is None:
                    return jsonify({
                        "message": Messages.ACCOUNT_NOT_EXIST
                    })
                
                return jsonify({
                    "account": account.to_dict()
                })
            except Exception as e:
                return jsonify(Messages.error(e))
            
    @staticmethod
    def account_update(payload, account_id, data):
        with Session() as session:
            try:
                account = session.query(Account).filter_by(id = account_id, user_id = payload["user_id"]).first()
                
                if account is None:
                    return jsonify({
                        "message": Messages.ACCOUNT_NOT_EXIST
                    }), 400
                    
                if data["account_number"] is not None:
                    account.account_number = data["account_number"]
                    
                session.commit()
                
                return jsonify({
                    "message": Messages.SUCCESS_UPDATE_ACCOUNT,
                    "account_updated": account.to_dict()
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400
    
    @staticmethod
    def account_delete(payload, account_id):
        with Session() as session:
            try:
                account_to_delete = session.query(Account).filter_by(id = account_id, user_id = payload["user_id"]).first()
                
                if account_to_delete is None:
                    return jsonify({
                        "message": Messages.ACCOUNT_NOT_EXIST
                    }), 404
                    
                account_to_delete.is_deleted = True
                
                session.commit()
                
                return jsonify({
                    "message": Messages.SUCCESS_DELETE_ACCOUNT
                })
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400
                
                
                