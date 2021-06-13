from flask import Flask
from flask_restplus import Api
from src.server.config import PRODUCTION, FLASK_PORT
from src.db_models.varejao.database import database_varejao
from src.db_models.macapa.database import database_macapa



class Server:
    def __init__(self):
        self.app = Flask(__name__)
        authorizations = {
            'apiKey': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Token'
            },
            'basic_auth': {
                'type': 'basic',
                'in': 'header',
                'name': 'Authorization'
            }
        }
        self.api = Api(
            self.app,
            authorizations=authorizations,
            version='1.0',
            title='contacts_api',
            description="API responsável por manter contatos",
            doc='/docs'
        )

    def run(self):
        database_varejao.init_db()
        database_macapa.init_db()
        self.app.run(host='0.0.0.0', port=FLASK_PORT, debug=not PRODUCTION)

server = Server()