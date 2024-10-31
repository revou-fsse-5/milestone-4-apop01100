from flask import jsonify
from app.connections.db import Session
from app.seeds.accounts_data import accounts_data
from app.seeds.transaction_data import transactions_data
from app.seeds.users_data import users_data
from app.models.accounts_model import Account
from app.models.transactions_model import Transaction
from app.models.users_model import User
from app.constant.messages import Messages
from sqlalchemy import text
from app.constant.query import Query

class SeedsService:
    @staticmethod
    def generate_all_data():
        new_users = []
        with Session() as session:
            try:
                # Check User Data
                check_users = session.query(User).count()
                
                # Check Account Data
                check_accounts = session.query(Account).count()
                
                # Check Transactions Data
                check_transactions = session.query(Transaction).count()
                
                if (check_users != 0) or (check_accounts != 0) or (check_transactions != 0):
                    return jsonify({
                        "message": "data already exist"
                    }), 400
                    
                # Generate User data
                for user in users_data:
                    new_user: User = User(
                        username=user["username"],
                        email=user["email"],
                        role=user["role"]
                    )
                    
                    new_user.set_password(user["password_hash"])
                    
                    new_users.append(new_user)
                    
                session.add_all(new_users)
                session.commit()
                
                # Generate Account Data
                new_accounts: Account = [Account(user_id=account["user_id"],
                                                 account_type=account["account_type"],
                                                 account_number=account["account_number"],
                                                 balance=account["balance"])
                                         for account in accounts_data]

                session.add_all(new_accounts)
                session.commit()
                
                # Geneare Transaction Data
                new_transactions: Transaction = [Transaction(from_account_id=transaction["from_account_id"],
                                                             to_account_id=transaction["to_account_id"],
                                                             amount=transaction["amount"],
                                                             type=transaction["type"],
                                                             description=transaction["description"])
                                                 for transaction in transactions_data]
                
                session.add_all(new_transactions)
                session.commit()
                
                return jsonify({
                    "message": Messages.SUCCESS_GENERATE_ALL_SEEDS
                }), 201
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400
    
    @staticmethod
    def show_data():
        with Session() as session:
            try:
                users =  session.query(User).all()
                list_users = [user.to_dict() for user in users]
                
                accounts = session.query(Account).all()
                list_accounts = [account.to_dict() for account in accounts]
                
                transactions = session.query(Transaction).all()
                list_transactions = [transaction.to_dict() for transaction in transactions]
                
                return jsonify({
                    "message": Messages.SUCCESS_SHOW_ALL_DATA,
                    "users": list_users,
                    "accounts": list_accounts,
                    "transactions": list_transactions
                })
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e))
    
    @staticmethod
    def clear_data():
        with Session() as session:
            try:
                session.query(Transaction).delete()
                session.execute(text(Query.reset_primary_key("transactions")))
                session.query(Account).delete()
                session.execute(text(Query.reset_primary_key("accounts")))
                session.query(User).delete()
                session.execute(text(Query.reset_primary_key("users")))
                
                session.commit()
                
                return jsonify({
                    "message": Messages.SUCCESS_CLEAR_ALL_DATA
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400
                