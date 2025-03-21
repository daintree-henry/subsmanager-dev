import os


class Config:
    # Construct database URI from individual components
    SUB_URL = os.getenv('SUB_URL')

    # Return Recommend Count
    RECOMMEND_COUNT = os.getenv('RECOMMEND_COUNT')

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')