import redis
from redis.connection import Connection, SSLConnection
from config import cfg

redis_client = redis.Redis()


connection_class = Connection
if cfg.REDIS_USE_SSL:
    connection_class = SSLConnection

redis_client.connection_pool = redis.ConnectionPool(**{
    'host': cfg.REDIS_HOST,
    'port': cfg.REDIS_PORT,
    'username': cfg.REDIS_USERNAME,
    'password': cfg.REDIS_PASSWORD,
    'db': cfg.REDIS_DB,
    'encoding': 'utf-8',
    'encoding_errors': 'strict',
    'decode_responses': False
}, connection_class=connection_class)

