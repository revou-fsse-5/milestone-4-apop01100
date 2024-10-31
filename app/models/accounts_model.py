from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Boolean, Enum
from app.constant.enums.account_type_enum import AccountTypeEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_type = Column(Enum(AccountTypeEnum), nullable=False)
    account_number = Column(String(10), unique=True, nullable=False)
    balance = Column(DECIMAL(10, 2), default=0.00, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    users = relationship("User", foreign_keys=[user_id], back_populates="accounts")
    
    outgoing_transactions = relationship("Transaction", foreign_keys='Transaction.from_account_id', back_populates="from_account")
    incoming_transactions = relationship("Transaction", foreign_keys='Transaction.to_account_id', back_populates="to_account")
    
    def to_dict(self):
        account = {
            "id": self.id,
            "user_id": self.user_id,
            "account_type": self.account_type,
            "account_number": self.account_number,
            "balance": self.balance,
            "metadata": {
                "creted_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
            }
        }
        
        return account