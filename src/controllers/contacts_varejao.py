from flask import request
from flask_restplus import Resource
from src.server.server import server
from src.db_models.varejao.contacts_varejao_model import ContactsVarejao, UserVarejao
from sqlalchemy import update, delete
from src.db_models.varejao.database import database_varejao
import json
from src.security.authentication import token_required, login_auth
from src.security.user_manager import UserManager
from src.utils.utils import return_message

api = server.api
app = server.app
db_session = database_varejao.db_session


@api.route('/varejao/contact')
class Contacts(Resource):

    @api.doc(security='apiKey')
    @token_required(UserVarejao)
    def get(self):
        return 'teste', 200


        # return UserManager.UserManager(payload, UserVarejao, db_session)
    def post(self):
        return 'Hello World!'


@api.route('/varejao/user')
class User(Resource):

    @login_auth(UserVarejao)
    def get(self):
        return UserManager.get_token(request.json, UserVarejao)

    def post(self):
        payload = request.json
        return UserManager.post(payload, UserVarejao, db_session)

    @login_auth(UserVarejao)
    def put(self):
        return UserManager.put(request.json, UserVarejao, db_session)

    @login_auth(UserVarejao)
    def delete(self):
        return UserManager.delete(request.json, UserVarejao, db_session)

    @login_auth(UserVarejao)
    def patch(self):
        return UserManager.update_token(request.json, UserVarejao, db_session)
