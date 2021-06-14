from math import ceil

from flask import request
from flask_restplus import Resource
from src.server.server import server
from src.db_models.macapa.contacts_macapa_model import ContactsMacapa, UserMacapa
from sqlalchemy import update, delete
from src.db_models.macapa.database import database_macapa
import json
from src.security.authentication import token_required, basic_auth
from src.security.user_manager import UserManager
from src.utils.utils import message_dict
import re


from src.rest_models.contact_rest_model import contact_rest_model_post, contact_fields_rest_model_get, \
    contact_rest_model_put, contact_rest_model_delete

from src.rest_models.user_rest_model import user_rest_model_get, user_rest_model_post, user_rest_model_put, token_model

from src.server.config import USE_CACHE
from src.cache.redis_handler import RedisHandler

api = server.api
db_session = database_macapa.db_session


@api.route('/macapa/contact')
class Contacts(Resource):

    @staticmethod
    def _format_cellphone_macapa(cellphone):
        only_numbers_cellphone = re.sub("[^0-9]", "", cellphone)
        formatted_cellphone = f'+{only_numbers_cellphone[:2]} ({only_numbers_cellphone[2:4]}) ' \
                              f'{only_numbers_cellphone[4:9]}-{only_numbers_cellphone[9:]}'
        return formatted_cellphone


    @staticmethod
    def _make_cache_key_for_macapa(key):
        return f'varejao-{key}'



    @api.doc(params={
        'page': 'Número da página',
        'per_page': 'Quantidade por pagina <= 100, default 50',
        "id": "Id do contato, informe para trazer apenas um"
    })
    @api.doc(responses={
        401: 'Unauthenticated',
        400: 'Bad request',
        404: 'Not found',
        500: 'Internal server error'
    })
    @api.response(200, 'Success', contact_fields_rest_model_get)
    @api.doc(security='apiKey')
    @token_required(UserMacapa)
    def get(self):
        try:
            per_page = request.args.get("per_page") if request.args.get("per_page") else 50
            page = request.args.get("page") if request.args.get("page") else 1

            try:
                page = int(page)
                per_page = int(per_page)

                page = 1 if page < 1 else page
                per_page = 1 if per_page < 1 else per_page
            except ValueError:
                return message_dict('Parâmetro página ou per_page inválido'), 400

            total = db_session.query(ContactsMacapa).count()
            if not total or total == 0:
                return message_dict('Não existem dados'), 404
            if ceil(total / per_page) < page:
                return message_dict('Página inexistente'), 400

            cache_results = None
            if USE_CACHE:
                redis_handler = RedisHandler()
                cache_key = f'per_page={per_page}page={page}' if not request.args.get("id") else request.args.get("id")
                cache_key = self._make_cache_key_for_macapa(cache_key)

                cache_results = redis_handler.get_value(cache_key)
                if cache_results:
                    cache_results = json.loads(cache_results)
            if cache_results:
                results = cache_results
            else:

                filtros = {}
                if request.args.get("id"):
                    filtros['id'] = request.args.get("id")

                results = db_session.query(ContactsMacapa).filter_by(**filtros) \
                    .limit(per_page).offset(per_page * (page - 1)).all()

                if not results:
                    return message_dict("Não existe nada para listar"), 404

                results = [{'id': result.id, "name": result.nome, "cellphone": result.celular} for result in results]

                if USE_CACHE:
                    cache_key = f'per_page={per_page}page={page}' if not request.args.get("id") \
                        else request.args.get("id")
                    cache_key = self._make_cache_key_for_macapa(cache_key)
                    redis_handler.set_value(cache_key, json.dumps(results))


            response = {"page": page, "total": total, "results_per_page": per_page, "contacts": results}
            return response, 200
        except Exception as e:
            return message_dict(str(e)), 500


    @api.doc(responses={
        401: 'Unauthenticated',
        400: 'Bad request',
        500: 'Internal server error',
    })
    @api.doc(security='apiKey')
    @api.expect(contact_rest_model_post, validate=True)
    @api.response(201, 'Success', [contact_fields_rest_model_get])
    @token_required(UserMacapa)
    def post(self):
        payload = request.json
        contacts = payload.get('contacts')


        validacao = []
        for contact in contacts:
            only_numbers_cellphone = re.sub("[^0-9]", "", contact.get('cellphone'))
            if len(only_numbers_cellphone) != 13:
                validacao.append(f'Formato de telefone inválido: {contact.get("cellphone")}, '
                                 f'name:{contact.get("name")}')
                continue


            formatted_cellphone = self._format_cellphone_macapa(only_numbers_cellphone)
            contact['cellphone'] = formatted_cellphone

        if validacao:
            return {"mensagem": "Erro ao validar os seguintes números", "numeros": validacao}, 400

        all_contacts = [
            ContactsMacapa(
                contact.get('name').upper(),
                contact.get('cellphone')
            )
            for contact in contacts]
        try:
            db_session.bulk_save_objects(all_contacts, return_defaults=True)
            db_session.commit()
            results = [{'id': contact.id, "name": contact.nome, "cellphone": contact.celular} for contact in
                       all_contacts]

            if USE_CACHE:
                redis_handler = RedisHandler()
                for result in results:
                    cache_key = self._make_cache_key_for_macapa(result['id'])
                    redis_handler.set_value(cache_key, json.dumps(result))

            return results, 201
        except Exception as e:
            return message_dict(str(e)), 500





    @api.doc(responses={
        401: 'Unauthenticated',
        400: 'Bad request',
        404: 'Not found',
        500: 'Internal server error',
        200: 'Success'
    })
    @api.expect(contact_rest_model_put, validate=True)
    @api.doc(security='apiKey')
    @token_required(UserMacapa)
    def put(self):

        payload = request.json

        contact_data = {}
        contact_data['id'] = payload['id']
        if 'name' in payload:
            contact_data['nome'] = payload['name'].upper()
        if 'cellphone' in payload:
            contact_data['celular'] = self._format_cellphone_macapa(payload['cellphone'])

        try:
            statement = update(ContactsMacapa).where(ContactsMacapa.id == contact_data['id']).values(contact_data). \
                execution_options(synchronize_session="fetch")

            result = db_session.execute(statement)
            num_rows_matched = result.rowcount
            db_session.commit()

            if num_rows_matched == 0:
                return message_dict("Contato inexistente"), 404

            if USE_CACHE:
                redis_handler = RedisHandler()
                cache_key = self._make_cache_key_for_macapa(contact_data['id'])
                redis_handler.delete_value(cache_key)

            return message_dict(f'Contato ID {contact_data["id"]} atualizado com sucesso'), 200
        except Exception as e:
            return message_dict(str(e)), 500

    @api.doc(responses={
        401: 'Unauthenticated',
        400: 'Bad request',
        404: 'Not found',
        500: 'Internal server error',
        200: 'Success'
    })
    @api.expect(contact_rest_model_delete, validate=True)
    @api.doc(security='apiKey')
    @token_required(UserMacapa)
    def delete(self):

        payload = request.json
        try:
            statement = delete(ContactsMacapa).where(ContactsMacapa.id == payload['id']). \
                execution_options(synchronize_session="fetch")

            result = db_session.execute(statement)
            num_rows_matched = result.rowcount
            db_session.commit()

            if num_rows_matched == 0:
                return message_dict(f"Contato ID: {payload['id']} não encontrado"), 404

            if USE_CACHE:
                redis_handler = RedisHandler()
                cache_key = self._make_cache_key_for_macapa(payload['id'])
                redis_handler.delete_value(cache_key)

            return message_dict(f'Contato ID: {payload["id"]} apagado com sucesso'), 200
        except Exception as e:
            return message_dict(str(e)), 500





@api.route('/macapa/user')
class User(Resource):

    @api.doc(responses={
        401: 'Unauthenticated',
        404: 'Not found',
        500: 'Internal server error'
    })
    @api.expect(user_rest_model_get, validate=True)
    @api.doc(description='Obtenha o token do respectivo usuário')
    @api.doc(security='basic_auth')
    @api.response(200, 'Success', token_model)
    @basic_auth(UserMacapa)
    def get(self):
        return UserManager.get_token(request.json, UserMacapa)

    @api.doc(responses={
        202: "Can't create duplicate",
        500: 'Internal server error',
        201: "Created"
    })
    @api.expect(user_rest_model_post, validate=True)
    @api.doc(description='Cadastre novo e-mail e senha')
    def post(self):
        payload = request.json
        return UserManager.post(payload, UserMacapa, db_session)

    @api.doc(responses={
        401: 'Unauthenticated',
        404: 'Not found',
        500: 'Internal server error',
        200: 'Success'
    })
    @api.expect(user_rest_model_put, validate=True)
    @api.doc(description='Atualize dados do cadastro, como nome e senha')
    @api.doc(security='basic_auth')
    @basic_auth(UserMacapa)
    def put(self):
        return UserManager.put(request.json, UserMacapa, db_session)

    @api.doc(responses={
        401: 'Unauthenticated',
        404: 'Not found',
        500: 'Internal server error',
        200: 'Success'
    })
    @api.expect(user_rest_model_get, validate=True)
    @api.doc(description='Delete seu cadastro pelo e-mail')
    @api.doc(security='basic_auth')
    @basic_auth(UserMacapa)
    def delete(self):
        return UserManager.delete(request.json, UserMacapa, db_session)

    @api.doc(responses={
        401: 'Unauthenticated',
        500: 'Internal server error'
    })
    @api.expect(user_rest_model_get, validate=True)
    @api.doc(description='Obtenha novo token, isso invalida o token anterior')
    @api.doc(security='basic_auth')
    @api.response(200, 'Success', token_model)
    @basic_auth(UserMacapa)
    def patch(self):
        return UserManager.update_token(request.json, UserMacapa, db_session)