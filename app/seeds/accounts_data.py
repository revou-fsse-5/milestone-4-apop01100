from datetime import datetime, timezone
from decimal import Decimal

# Seed data for Account model
accounts_data = [
    {
        "user_id": 1,
        "account_type": "SAVING",
        "account_number": "1234567890",
        "balance": Decimal("5000000.00"),  # in Rupiah
    },
    {
        "user_id": 2,
        "account_type": "TRANSACTIONAL",
        "account_number": "0987654321",
        "balance": Decimal("2500000.00"),  # in Rupiah
    }
]