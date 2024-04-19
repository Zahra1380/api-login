from passlib.context import CryptContext
from datetime import timedelta

import redis

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
JWT_SECRET_KEY = '$JWT_SECRET_KEY'
#ACCESS_EXPIRES = timedelta(seconds=30)
ACCESS_EXPIRES = 60

REFRESH_EXPIRES = timedelta(days=30)

# redis setup
redis_conn = redis.Redis(host='redis', port=6379, db=0)