from enum import Enum

class TransactionTypeEnum(str, Enum):
    TRANSFER = "transfer"
    DEPOSIT = "deposit"
    INVESTMENT = "investment"
    WITHDRAWAL = "withdrawal"

    
    @classmethod
    def get_all_transaction_type(cls):
        types = list(cls)
        type_values = {type.value for type  in types}
        
        return type_values