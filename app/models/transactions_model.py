from app.connections.db import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, DECIMAL, Text, Enum
from app.constant.enums.transaction_type_enum import TransactionTypeEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, nullable=False)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    type = Column(Enum(TransactionTypeEnum), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=None, onupdate=datetime.now(timezone.utc), nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    from_account = relationship("Account", foreign_keys=[from_account_id], back_populates="outgoing_transactions")
    to_account = relationship("Account", foreign_keys=[to_account_id], back_populates="incoming_transactions")
    
    def to_dict(self):
        user = {
            "id": self.id,
            "from_account_id": self.from_account_id,
            "to_account_id": self.to_account_id,
            "amount": self.amount,
            "type": self.type,
            "description": self.description,
            "metadata": {
                "creted_at": self.created_at,
                "updated_at": self.updated_at,
                "is_deleted": self.is_deleted
            }
        }
        
        return user