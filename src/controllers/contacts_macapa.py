from flask import request
from flask_restplus import Resource
from src.server.server import server
from src.db_models.macapa.contacts_macapa_model import ContactsMacapa
from sqlalchemy import update, delete
from src.db_models.macapa.database import database_macapa
import json


api = server.api
db_session = database_macapa.db_session


@api.route('/contacts/macapa')
class Contacts(Resource):
    def get(self):
        return 'Hello World!'