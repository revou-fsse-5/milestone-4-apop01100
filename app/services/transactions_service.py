from flask import jsonify
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app.models.users_model import User
from app.models.transactions_model import Transaction
from app.models.accounts_model import Account
from app.connections.db import Session
from app.constant.messages import Messages
from decimal import Decimal

class TransactionsService:
    @staticmethod
    def show_transactions(payload):
        with Session() as session:
            try:
                if payload["role"] == "admin":
                    transactions = session.query(Transaction).all()
                    list_transactions = [transaction.to_dict() for transaction in transactions]
                
                if payload["role"] == "user":
                    user_transactions = (
                            session.query(User)
                            .options(
                                joinedload(User.accounts)
                                .joinedload(Account.incoming_transactions)
                            )
                            .options(
                                joinedload(User.accounts)
                                .joinedload(Account.outgoing_transactions)
                            )
                            .filter_by(id = payload["user_id"])
                            .all()
                        )
                        
                    list_transactions = [user_transaction.to_dict() for user_transaction in user_transactions]
                
                return jsonify({
                        "transactions": list_transactions,
                        "message": Messages.SUCCESS_SHOW_ALL_TRANSACTIONS
                    }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400
            
    @staticmethod
    def transaction_detail(payload, transaction_id):
        with Session() as session:
            try:
                if payload["role"] == "admin":
                    transaction = session.query(Transaction).filter_by(id = transaction_id).first()
                    
                if payload["role"] == "user":
                    transaction = (
                            session.query(User)
                            .options(
                                joinedload(User.accounts)
                                .joinedload(Account.incoming_transactions)
                            )
                            .options(
                                joinedload(User.accounts)
                                .joinedload(Account.outgoing_transactions)
                            )
                            .filter(User.id == payload["user_id"])
                            .filter(Account.id == transaction_id).first()
                        )
                    
                if transaction is None:
                    return jsonify({
                        "messages": Messages.TRANSACTION_NOT_FOUND
                    })
                    
                return jsonify({
                    "transaction": transaction.to_dict(),
                    "message": Messages.SUCCESS_SHOW_TRANSACTION
                })
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e))
            
    @staticmethod
    def transfer_transaction(payload, data):
        with Session() as session:
            try:
                # get account from_account
                from_account = session.query(Account).filter_by(account_type="transactional", 
                                                                user_id=payload["user_id"], 
                                                                account_number=data["from_account_number"]).first()
                # get id to_number_account                                                      
                to_account = session.query(Account).filter_by(account_type="transactional",
                                                              account_number=data["to_account_number"]).first()
                
                if from_account is None:
                    return jsonify({
                        "message": f"your transactional {Messages.ACCOUNT_NOT_EXIST}"
                    }), 400
                    
                if to_account is None:
                    return jsonify({
                        "message": f"your beneficeary {Messages.ACCOUNT_NOT_EXIST}"
                    }), 400
                
                if from_account.id == to_account.id:
                    return jsonify({
                        "message": Messages.CANNOT_TRANSFER_SAME_ID
                    }), 400
                
                # check balance
                account_balance = from_account.balance
                amount = Decimal(data["amount"])
                if amount > account_balance:
                    return jsonify({
                        "message": Messages.INSUFFICIENT_BALANCE
                    }), 400
                    
                    
                new_balance = account_balance - amount
                
                from_account.balance = new_balance
                to_account.balance += amount
                
                new_transaction = Transaction(from_account_id=from_account.id,
                                            to_account_id=to_account.id,
                                            amount=amount,
                                            type="transfer",
                                            description=data["description"])
                
                session.add(new_transaction)            
                session.commit()
                
                return jsonify({
                    "message": f"transfer {Messages.TRANSACTION_SUCCESS}",
                    "new_transaction": new_transaction.to_dict()
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e)), 400
            
    @staticmethod
    def withdrawal_transaction(payload, data):
        with Session() as session:
            try:
                # check account
                withdrawal_account = session.query(Account).filter_by(account_type="transactional",
                                                                      user_id=payload["user_id"],
                                                                      account_number=data["from_account_number"]).first()
                
                if withdrawal_account is None:
                    return jsonify({
                        "message": f"transactional {Messages.ACCOUNT_NOT_EXIST}"
                    }), 400
                    
                # balance check
                balance = withdrawal_account.balance
                amount = Decimal(data["amount"])
                if amount > balance:
                    return jsonify({
                        "message": Messages.INSUFFICIENT_BALANCE
                    }), 400
                new_balance = balance - amount
                
                withdrawal_account.balance = new_balance
                
                new_transaction = Transaction(from_account_id=withdrawal_account.id,
                                              to_account_id=withdrawal_account.id,
                                              amount=amount,
                                              type="withdrawal",
                                              description=data["description"])
                
                session.add(new_transaction)
                session.commit()
                
                return jsonify({
                    "message": f"withdrawal {Messages.TRANSACTION_SUCCESS}",
                    "new_transaction": new_transaction.to_dict()
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e))    
            
    @staticmethod
    def deposit_transaction(payload, data):
        with Session() as session:
            try:
                # check deposit account
                deposit_account = session.query(Account).filter_by(user_id = payload["user_id"],
                                                                   account_number=data["from_account_number"]).first()
                
                if deposit_account is None:
                    return jsonify({
                        "message": Messages.ACCOUNT_NOT_EXIST
                    }), 400
                
                amount = Decimal(data["amount"])
                deposit_account.balance += amount
                
                new_transaction = Transaction(from_account_id=deposit_account.id,
                                              to_account_id=deposit_account.id,
                                              amount=amount,
                                              type="deposit",
                                              description=data["description"])
                
                session.add(new_transaction)
                session.commit()
                
                return jsonify({
                    "message": f"deposit {Messages.TRANSACTION_SUCCESS}",
                    "new_transacton": new_transaction.to_dict()
                }), 200
            except Exception as e:
                session.rollback()
                return jsonify(Messages.error(e))         
