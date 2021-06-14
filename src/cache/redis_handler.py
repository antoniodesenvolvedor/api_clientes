import redis
from src.server.config import REDIS_HOST, REDIS_PORT, REDIS_DATABASE, REDIS_TTL

class RedisHandler:
    def __init__(self):
        self._redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE)
        self._ttl = REDIS_TTL

    def get_value(self, name):
        value = self._redis.get(name)
        if value:
            return value.decode("utf-8")

    def set_value(self, name, value):
        self._redis.set(name=name, value=value, ex=self._ttl)

    def delete_value(self, name):
        self._redis.delete(name)