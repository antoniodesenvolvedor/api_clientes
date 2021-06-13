
from flask_restplus import fields
from src.server.server import server

user_rest_model_get = server.api.model(
    "user_rest_model_get",
    {
        "email": fields.String(description="Email do usuário", required=True)
     }
)


user_rest_model_post = server.api.model(
    "user_rest_model_post",
    {
        "email": fields.String(description="Email do usuário", required=True),
        "password": fields.String(description="Password do usuário", required=True),
        "name": fields.String(description="Nome do usuário", required=True)
     }
)

user_rest_model_put = server.api.model(
    "user_rest_model_put",
    {
        "email": fields.String(description="Email do usuário", required=True),
        "password": fields.String(description="Password do usuário"),
        "name": fields.String(description="Nome do usuário")
     }
)

token_model = server.api.model(
    "token_model",
    {
        "token": fields.String(description="Token do usuário"),

     }
)
