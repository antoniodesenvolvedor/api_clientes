from functools import wraps
from flask import request
import jwt
from src.server.config import TOKEN_KEY
from werkzeug.security import check_password_hash
from src.utils.utils import return_message

def token_required(UserModel):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None

            if 'Token' in request.headers:
                token = request.headers['Token']
            if not token:
                return return_message('Token is missing !!'), 401

            try:
                data = jwt.decode(token, TOKEN_KEY, algorithms=["HS256"])
                UserModel.query \
                    .filter_by(public_id=data['public_id']) \
                    .first()
            except Exception:
                return return_message('Token is invalid !!'), 401
            return f(*args, **kwargs)
        return decorated
    return decorator




def login_auth(UserModel):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            try:
                payload = request.json
            except:
                return return_message('É necessário importar uma payload válida'), 400

            if not payload or not payload.get('email') or not payload.get('password'):
                return return_message('É necessário informar os parâmetros email e password no payload'), 401

            user = UserModel.query.filter_by(email=payload.get('email')).first()

            if not user:
                return return_message('email ou senha inválidos'), 401,

            if not check_password_hash(user.password, payload.get('password')):
                return return_message('email ou senha inválidos'), 401

            return f(*args, **kwargs)
        return decorated
    return decorator
