import redis
import logging
from django.conf import settings

logger = logging.getLogger(__name__)
class RedisClient:
    def __init__(self):
        """
        Initializes the Redis client.
        """
        try:
            self.redis = redis.StrictRedis(
                host=settings.REDIS_HOST,      # Example: 'localhost' or Redis server IP
                port=settings.REDIS_PORT,      # Example: 6379
                db=settings.REDIS_DB,          # Example: 0
                decode_responses=True          # Ensures values are returned as strings
            )
            self.redis.ping()  # Test connection
            logger.info("✅ Connected to Redis successfully.")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            raise Exception(f"Redis connection error: {e}")

    def get(self, key):
        """
        Get a value from Redis by key.
        """
        try:
            value = self.redis.get(key)
            return value
        except Exception as e:
            logger.error(f"❌ Redis get failed for key {key}: {e}")
            return None

    def set(self, key, value, expiry=None):
        """
        Set a value in Redis with optional expiry (in seconds).
        """
        try:
            if expiry:
                self.redis.setex(key, expiry, value)
            else:
                self.redis.set(key, value)
            return True
        except Exception as e:
            logger.error(f"❌ Redis set failed for key {key}: {e}")
            return False

    def delete(self, key):
        """
        Delete a key from Redis.
        """
        try:
            return self.redis.delete(key)
        except Exception as e:
            logger.error(f"❌ Redis delete failed for key {key}: {e}")
            return False