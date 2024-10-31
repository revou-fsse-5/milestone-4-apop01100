from pydantic import BaseModel, condecimal, Field
from decimal import Decimal
from app.constant.enums.user_role_enum import RoleUserEnum
from app.constant.enums.account_type_enum import AccountTypeEnum
from app.constant.enums.transaction_type_enum import TransactionTypeEnum

ConstrainedDecimal = condecimal(max_digits=10, decimal_places=2)

class LoginValidator(BaseModel):
    username: str
    password: str
    
class RegisterValidator(BaseModel):
    username: str
    email: str
    role: RoleUserEnum
    password_hash: str
    
class CreateAccountValidator(BaseModel):
    user_id: int
    account_type: AccountTypeEnum
    
class UpdateUserValidator(BaseModel):
    username: str = None
    email: str = None
    password: str = None
    
class UpdateAccountValidator(BaseModel):
    account_number: str
    
class CreateTransactionValidator(BaseModel):
    from_account_number: str
    to_account_number: str = None
    amount: Decimal
    transaction_type: TransactionTypeEnum
    description: str = None
    
    