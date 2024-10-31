import os
from datetime import timedelta

class Config:
    SECRET_KEY  = os.getenv("SECRET_KEY")

class DevelopmentConfig():
    DEBUG = True
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
class ProductionConfig():
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
class TestConfig():
    TESTING = True