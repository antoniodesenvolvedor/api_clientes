from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from src.server.config import TOKEN_KEY
from datetime import datetime, timedelta
from flask import request
import uuid
from sqlalchemy import update, delete
from functools import wraps
from src.utils.utils import return_message

class UserManager:

    @staticmethod
    def get_token(payload, UserModel):
        email = payload.get('email')
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            return return_message("E-mail não encontrado"), 404

        token = jwt.encode({
            'public_id': user.public_id,
        }, TOKEN_KEY, algorithm="HS256")

        return return_message({'token': token}), 200


    @staticmethod
    def post(payload, UserModel, db_session):

        name = payload.get('name')
        email = payload.get('email')
        password = payload.get('password')

        user = UserModel.query \
            .filter_by(email=email) \
            .first()
        if user:
            return return_message('Email já cadastrado'), 202

        user = UserModel(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password)
        )
        db_session.add(user)
        db_session.commit()

        return return_message('Usuário cadastrado com sucesso'), 201

    @staticmethod
    def delete(payload, UserModel, db_session):
        if not payload or not payload.get('email'):
            return return_message('É necessário informar os parâmetros email no payload'), 401

        statement = delete(UserModel).where(UserModel.email == payload.get('email')).\
            execution_options(synchronize_session="fetch")

        result = db_session.execute(statement)
        num_rows_matched = result.rowcount
        db_session.commit()

        if num_rows_matched == 0:
            return return_message("E-mail não encontrado"), 404

        return return_message(f"E-mail {payload.get('email')} apagado com sucesso"), 200

    @staticmethod
    def put(payload, UserModel, db_session):
        if not payload or not payload.get('email'):
            return return_message('É necessário informar os parâmetros email" no payload'), 401

        name = payload.get('name')
        password = generate_password_hash(payload.get('password'))

        user_data = {}
        if 'name' in payload:
            user_data['name'] = name
        if 'password' in payload:
            user_data['password'] = password


        statement = update(UserModel).where(UserModel.email == payload.get('email')). \
            values(user_data).execution_options(synchronize_session="fetch")

        result = db_session.execute(statement)
        num_rows_matched = result.rowcount
        db_session.commit()

        if num_rows_matched == 0:
            return return_message("E-mail não encontrado"), 404

        return return_message(f"E-mail {payload.get('email')} atualizado com sucesso"), 200

    @staticmethod
    def update_token(payload, UserModel, db_session):
        if not payload or not payload.get('email'):
            return return_message('É necessário informar os parâmetros email no payload'), 401

        statement = update(UserModel).where(UserModel.email == payload.get('email')). \
            values({'public_id': str(uuid.uuid4())}).execution_options(synchronize_session="fetch")

        result = db_session.execute(statement)
        num_rows_matched = result.rowcount
        db_session.commit()

        if num_rows_matched == 0:
            return return_message("Erro ao atualizar o token"), 500

        user = UserModel.query.filter_by(email=payload.get('email')).first()

        token = jwt.encode({
            'public_id': user.public_id,
        }, TOKEN_KEY, algorithm="HS256")

        return return_message({'token': token}), 200




