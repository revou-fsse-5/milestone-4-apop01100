from enum import Enum

class RoleUserEnum(str, Enum):
    ADMIN = "admin"
    USER = "user"
    SUPER_ADMIN = "super_admin"
    
    @classmethod
    def get_all_roles(cls):
        roles = list(cls)
        roles_value = {role.value for role  in roles}
        
        return roles_value