from datetime import datetime, timezone

# Seed data for User model
users_data = [
    {
        "username": "user1",
        "email": "user1@example.com",
        "role": "USER",  # assuming RoleUserEnum.USER
        "password_hash": "hashed_password1"
    },
    {
        "username": "user2",
        "email": "user2@example.com",
        "role": "USER",  # assuming RoleUserEnum.USER
        "password_hash": "hashed_password2"
    },
    {
        "username": "admin1",
        "email": "admin1@example.com",
        "role": "ADMIN", # assuming RoleUserEnum.ADMIN
        "password_hash": "hashed_password3"
    },
    {
      "username": "super_admin",
      "email": "superadmin@example.com",
      "role": "SUPER_ADMIN", # assuming RoleUserEnum.SUPER_ADMIN
      "password_hash": "hashed_password4"  
    }
]
