from datetime import datetime, timezone
from decimal import Decimal

# Seed data for Transaction model
transactions_data = [
    {
        "from_account_id": 1,
        "to_account_id": 2,
        "amount": Decimal("500000.00"),  # in Rupiah
        "type": "TRANSFER",
        "description": "Payment for services"
    },
    {
        "from_account_id": 2,
        "to_account_id": 1,
        "amount": Decimal("150000.00"),  # in Rupiah
        "type": "INVESTMENT",
        "description": "Refund for overcharge"
    }
]
