from flask import Flask
from flask_restplus import Api
from src.config import PRODUCTION, FLASK_PORT


class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(
            self.app,
            version='1.0',
            title='contacts_api',
            description="API responsável por manter contatos",
            doc='/docs'
        )

    def run(self):
        self.app.run(host='0.0.0.0', port=FLASK_PORT, debug=not PRODUCTION)

server = Server()