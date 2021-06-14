import os
from dotenv import load_dotenv

load_dotenv()

PRODUCTION = os.getenv('PRODUCTION') == '1'
FLASK_PORT = os.getenv('FLASK_PORT')


_POSTGRES_USER = os.getenv('POSTGRES_USER')
_POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
_POSTGRES_DB = os.getenv('POSTGRES_DB')
_POSTGRES_PORT = os.getenv('POSTGRES_PORT')

_postgres_sql_host = 'postgres_mercafacil' if PRODUCTION else 'localhost'
CONNECTION_STRING_POSTGRES = f'postgresql+psycopg2://{_POSTGRES_USER}:{_POSTGRES_PASSWORD}' \
                             f'@{_postgres_sql_host}:{_POSTGRES_PORT}/{_POSTGRES_DB}'


_MYSQL_USER = os.getenv('MYSQL_USER')
_MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
_MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
_MYSQL_PORT = os.getenv('MYSQL_PORT')


_my_sql_host = 'mysql_mercafacil' if PRODUCTION else 'localhost'
CONNECTION_STRING_MYSQL = f'mysql+mysqlconnector://{_MYSQL_USER}:{_MYSQL_PASSWORD}' \
                             f'@{_my_sql_host}:{_MYSQL_PORT}/{_MYSQL_DATABASE}'

print(CONNECTION_STRING_MYSQL)


TOKEN_KEY = os.getenv('TOKEN_KEY')

REDIS_HOST = os.getenv('REDIS_HOST') if PRODUCTION else 'localhost'
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DATABASE = os.getenv('REDIS_DATABASE')
REDIS_TTL = os.getenv('REDIS_TTL')
USE_CACHE = os.getenv('USE_CACHE') == '1'




