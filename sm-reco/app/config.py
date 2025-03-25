import os


class Config:
    # Construct database URI from individual components
    SUB_URL = os.getenv('SUB_URL', 'http://sm-subs')

    # Return Recommend Count
    RECOMMEND_COUNT = os.getenv('RECOMMEND_COUNT', '1')

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'mJMLk2qwEFKp1Lx2FatzwVOA6-3FjMqkLEAWu74uCU9')

    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'redispassword')

    CACHE_KEY = os.getenv('CACHE_KEY', 'SUB_PLANS')
    CACHE_TTL_SECOND = int(os.getenv('CACHE_TTL_SECOND', '60'))