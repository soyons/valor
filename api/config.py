import os

import dotenv

dotenv.load_dotenv()

DEFAULTS = {
    'EDITION': 'SELF_HOSTED',
    'SECRET_KEY': 'SECRET_KEY',
    'ALGORITHM': 'HS256',
    'ACCESS_TOKEN_EXPIRE_MINUTES': 300,
    'DB_USERNAME': 'valor',
    'DB_PASSWORD': '',
    'DB_HOST': 'localhost',
    'DB_PORT': '5432',
    'DB_DATABASE': 'dify',
    'DB_CHARSET': '',
    'REDIS_HOST': 'localhost',
    'REDIS_PORT': '6379',
    'REDIS_DB': '0',
    'REDIS_USE_SSL': 'False',
    'SQLALCHEMY_POOL_SIZE': 30,
    'SQLALCHEMY_MAX_OVERFLOW': 10,
    'SQLALCHEMY_POOL_RECYCLE': 3600,
    'SQLALCHEMY_ECHO': 'False',
    'LOG_LEVEL': 'INFO',
    'LOG_FILE': '',
    'LOG_FORMAT': '%(asctime)s.%(msecs)03d %(levelname)s [%(threadName)s] [%(filename)s:%(lineno)d] - %(message)s',
    'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S',
    'DEPLOY_ENV': 'PRODUCTION',
}


def get_env(key):
    return os.environ.get(key, DEFAULTS.get(key))


def get_bool_env(key):
    value = get_env(key)
    return value.lower() == 'true' if value is not None else False


def get_cors_allow_origins(env, default):
    cors_allow_origins = []
    if get_env(env):
        for origin in get_env(env).split(','):
            cors_allow_origins.append(origin)
    else:
        cors_allow_origins = [default]

    return cors_allow_origins


class Config:
    """Application configuration class."""

    def __init__(self):
        # ------------------------
        # General Configurations.
        # ------------------------
        self.CURRENT_VERSION = "0.0.1"
        self.COMMIT_SHA = get_env('COMMIT_SHA')
        self.EDITION = get_env('EDITION')
        self.DEPLOY_ENV = get_env('DEPLOY_ENV')
        self.TESTING = False
        self.LOG_LEVEL = get_env('LOG_LEVEL')
        self.LOG_FILE = get_env('LOG_FILE')
        self.LOG_FORMAT = get_env('LOG_FORMAT')
        self.LOG_DATEFORMAT = get_env('LOG_DATEFORMAT')
        self.SECRET_KEY = get_env('SECRET_KEY')
        self.ALGORITHM = get_env('ALGORITHM')
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env('ACCESS_TOKEN_EXPIRE_MINUTES'))

        # cors settings
        self.WEB_API_CORS_ALLOW_ORIGINS = get_cors_allow_origins(
            'WEB_API_CORS_ALLOW_ORIGINS', '*')

        # ------------------------
        # Database Configurations.
        # ------------------------
        db_credentials = {
            key: get_env(key) for key in
            ['DB_USERNAME', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_DATABASE', 'DB_CHARSET']
        }

        db_extras = f"?client_encoding={db_credentials['DB_CHARSET']}" if db_credentials['DB_CHARSET'] else ""

        self.SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{db_credentials['DB_USERNAME']}:{db_credentials['DB_PASSWORD']}@{db_credentials['DB_HOST']}:{db_credentials['DB_PORT']}/{db_credentials['DB_DATABASE']}{db_extras}"
        # print(self.SQLALCHEMY_DATABASE_URL)
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': int(get_env('SQLALCHEMY_POOL_SIZE')),
            'max_overflow': int(get_env('SQLALCHEMY_MAX_OVERFLOW')),
            'pool_recycle': int(get_env('SQLALCHEMY_POOL_RECYCLE'))
        }

        self.SQLALCHEMY_ECHO = get_bool_env('SQLALCHEMY_ECHO')

        # ------------------------
        # Redis Configurations.
        # ------------------------
        self.REDIS_HOST = get_env('REDIS_HOST')
        self.REDIS_PORT = get_env('REDIS_PORT')
        self.REDIS_USERNAME = get_env('REDIS_USERNAME')
        self.REDIS_PASSWORD = get_env('REDIS_PASSWORD')
        self.REDIS_DB = get_env('REDIS_DB')
        self.REDIS_USE_SSL = get_bool_env('REDIS_USE_SSL')


cfg = Config()