class Messages:
    USERNAME_ALREADY_EXIST = "username already exist"
    EMAIL_ALREADY_EXIST = "email already exist"
    CREATE_USER_SUCCESS = "success create new user"
    ROLE_NOT_EXIST = "role not exist"
    SUCCESS_GENERATE_ALL_SEEDS = "success generate all seeds"
    SUCCESS_SHOW_ALL_DATA = "success show all data"
    SUCCESS_CLEAR_ALL_DATA = "success clear all data"
    SUCCESS_CREATE_ACCOUNT = "success create account"
    SUCCESS_UPDATE_USER = "success update user"
    SUCCESS_UPDATE_ACCOUNT = "success update account"
    SUCCESS_DELETE_ACCOUNT = "success delete account"
    SUCCESS_SHOW_ALL_TRANSACTIONS = "success show all transactions"
    SUCCESS_SHOW_TRANSACTION = "success show transaction"
    ACCOUNT_NOT_EXIST = "account not exist"
    CANNOT_TRANSFER_SAME_ID = "cannot transfer for the sama number"
    INSUFFICIENT_BALANCE = "account insufficient balance"
    TRANSACTION_NOT_FOUND = "transaction not found"
    TRANSACTION_SUCCESS = "transaction success"
    ROLE_NOT_AUTHORIZED = "role not authorizes"
    USERNAME_NOT_FOUND = "username not found"
    INCORRECT_PASSWORD = "incorrect password"
    LOGIN_SUCCESS = "login succes"
    
    @staticmethod
    def error(e):
        return {"error": f"{e}"}