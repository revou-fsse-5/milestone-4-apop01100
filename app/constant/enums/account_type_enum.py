from enum import Enum

class AccountTypeEnum(str, Enum):
    TRANSACTIONAL = "transactional"
    SAVING = "saving"
    
    @classmethod
    def get_all_account_type(cls):
        types = list(cls)
        type_values = {type.value for type in types}
        
        return type_values