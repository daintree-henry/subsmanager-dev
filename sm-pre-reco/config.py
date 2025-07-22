import os


class Config:
    SUB_URL = os.getenv('SUB_URL', 'http://sm-subs')
    USER_URL = os.getenv('USER_URL', 'http://sm-user')

    REDIS_HOST = os.getenv('REDIS_HOST', 'sm-redis')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'redispassword')

    RECOMMEND_COUNT = os.getenv('RECOMMEND_COUNT', '1')
    RECOMMEND_CACHE_TTL_SECOND = int(os.getenv('RECOMMEND_CACHE_TTL_SECOND', '86400'))
    
    # Fixed secret key for internal service-to-service calls
    INTERNAL_SECRET = 'secret123'