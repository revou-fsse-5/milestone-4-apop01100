import random

def generate_random_account_number(length=10):
    return ''.join(random.choices('0123456789', k=length))