from flask import Blueprint
from app.controllers.users_controllers import UsersController
from app.controllers.accounts_controllers import AccountsControllers
from app.controllers.transactions_controllers import TransactionControllers
from app.controllers.seeds_controllers import seeds_controller

users = Blueprint("users", __name__)
users.add_url_rule("/register/<string:role>", view_func=UsersController.create_user, methods=["POST"])
users.add_url_rule("/login", view_func=UsersController.login_user, methods=["POST"])
users.add_url_rule("/me", view_func=UsersController.user_profile, methods=["GET"])
users.add_url_rule("/me", view_func=UsersController.user_update, methods=["PUT"])

accounts = Blueprint("accounts", __name__)
accounts.add_url_rule("/", view_func=AccountsControllers.create_account, methods=["POST"])
accounts.add_url_rule("/", view_func=AccountsControllers.show_accounts, methods=["GET"])
accounts.add_url_rule("/<int:id>", view_func=AccountsControllers.show_account_detail, methods=["GET"])
accounts.add_url_rule("/<int:id>", view_func=AccountsControllers.account_update, methods=["PUT"])
accounts.add_url_rule("/<int:id>", view_func=AccountsControllers.account_delete, methods=["DELETE"])

transactions = Blueprint("transactions", __name__)
transactions.add_url_rule("/", view_func=TransactionControllers.show_all_transaction, methods=["GET"])
transactions.add_url_rule("/<int:id>", view_func=TransactionControllers.transaction_detail, methods=["GET"])
transactions.add_url_rule("/", view_func=TransactionControllers.create_transaction, methods=["POST"])

seeds = Blueprint("seeds", __name__)
seeds.add_url_rule("/", view_func=seeds_controller, methods=["GET", "POST", "DELETE"])