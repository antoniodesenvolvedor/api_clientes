from functools import wraps
from flask import request
import jwt
from src.server.config import TOKEN_KEY
from werkzeug.security import check_password_hash
from src.utils.utils import message_dict

def token_required(UserModel):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'Token' in request.headers:
                token = request.headers['Token']
            if not token:
                return message_dict('É necessário informar o token !!'), 401

            try:
                data = jwt.decode(token, TOKEN_KEY, algorithms=["HS256"])
                user = UserModel.query \
                    .filter_by(public_id=data['public_id']) \
                    .first()

                if not user:
                    return message_dict('Token inválido!!'), 401
            except Exception:
                return message_dict('Token inválido !!'), 401
            return f(*args, **kwargs)
        return decorated
    return decorator




def basic_auth(UserModel):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                if not request.authorization:
                    raise ValueError("É necessário informar uma basic auth")

                email = request.authorization.username
                password = request.authorization.password
                email_body = request.json.get('email')

                if not email or not password:
                    raise ValueError("É necessário informar uma basic auth")
                if not email_body:
                    raise ValueError("É necessário informar o e-mail no payload")

            except ValueError as error:
                return message_dict(str(error)), 401
            except Exception as e:
                return message_dict(str(e)), 500

            if email != email_body:
                return message_dict('O email da autenticação dever ser o mesmo da operação'), 401

            user = UserModel.query.filter_by(email=email).first()

            if not user:
                return message_dict('email ou senha inválidos'), 401,

            if not check_password_hash(user.password, password):
                return message_dict('email ou senha inválidos'), 401

            return f(*args, **kwargs)
        return decorated
    return decorator
