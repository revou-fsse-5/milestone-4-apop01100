from flask import Flask, redirect
from app.config import DevelopmentConfig, ProductionConfig
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from app.models.users_model import User
from app.models.transactions_model import Transaction
from app.models.accounts_model import Account
from app.connections.db import Base, engine
import os

jwt = JWTManager()

def create_app(test_config=None, production_config=os.getenv("PRODUCTION_CONFIG")):
    app = Flask(__name__)
    
    Base.metadata.create_all(engine)
    
    if test_config is not None:
        app.config.from_object(test_config)
    if production_config is not None:
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
        
    jwt.init_app(app)
    swagger = Swagger(app)
    
    @app.route("/")
    def index():
        return redirect("https://documenter.getpostman.com/view/31842216/2sAY4vhhyw")
    
    from app.router import users, accounts, transactions, seeds
    app.register_blueprint(users, url_prefix="/users")
    app.register_blueprint(accounts, url_prefix="/accounts")
    app.register_blueprint(transactions, url_prefix="/transactions")
    app.register_blueprint(seeds, url_prefix="/seeds")
    
    return app