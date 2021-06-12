import os
from dotenv import load_dotenv

load_dotenv()

PRODUCTION = os.getenv('PRODUCTION') == '1'
FLASK_PORT = os.getenv('FLASK_PORT')


_POSTGRES_USER = os.getenv('POSTGRES_USER')
_POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
_POSTGRES_DB = os.getenv('POSTGRES_DB')
_POSTGRES_PORT = os.getenv('POSTGRES_PORT')

CONNECTION_STRING_POSTGRES = f'postgresql+psycopg2://{_POSTGRES_USER}:{_POSTGRES_PASSWORD}' \
                             f'@postgres_mercafacil:{_POSTGRES_PORT}/{_POSTGRES_DB}'
CONNECTION_STRING_POSTGRES_DEV = f'postgresql+psycopg2://{_POSTGRES_USER}:{_POSTGRES_PASSWORD}' \
                                 f'@localhost:{_POSTGRES_PORT}/{_POSTGRES_DB}'

_MYSQL_USER = os.getenv('MYSQL_USER')
_MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
_MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
_MYSQL_PORT = os.getenv('MYSQL_PORT')

CONNECTION_STRING_MYSQL = f'mysql+mysqlconnector://{_MYSQL_USER}:{_MYSQL_PASSWORD}' \
                             f'@mysql_mercafacil:{_MYSQL_PORT}/{_MYSQL_DATABASE}'
CONNECTION_STRING_MYSQL_DEV = f'mysql+mysqlconnector://{_MYSQL_USER}:{_MYSQL_PASSWORD}' \
                                 f'@localhost:{_MYSQL_PORT}/{_MYSQL_DATABASE}'


TOKEN_KEY = os.getenv('TOKEN_KEY')




