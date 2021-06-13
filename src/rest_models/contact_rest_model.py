from flask_restplus import fields
from src.server.server import server


contact_fields_rest_model_get = server.api.model(
    'contact_fields_rest_model_get', {
    "id": fields.Integer(description="ID do contato"),
    "name": fields.String(description="Nome do contato"),
    "cellphone": fields.String(description="Celular do contato"),
})

contact_rest_model_get = server.api.model(
    "contact_rest_model_get",
    {
        "page": fields.Integer(description="Número da página"),
        "total": fields.Integer(description="Total de páginas"),
        "results_per_page": fields.Integer(description="Quantidade de registros por página"),
        "contacts": fields.List(fields.Nested(contact_fields_rest_model_get))
     }
)

contact_fields_rest_model_post = server.api.model(
    'contact_fields_rest_model_post', {
    "name": fields.String(description="Nome do contato", required=True),
    "cellphone": fields.String(description="Celular do contato", required=True),
})

contact_rest_model_post = server.api.model(
    "contact_rest_model_post",
    {
        "contacts": fields.List(fields.Nested(contact_fields_rest_model_post))
     }
)

contact_rest_model_put = server.api.model(
    'contact_rest_model_put', {
    "id": fields.Integer(description="ID do contato", required=True),
    "name": fields.String(description="Nome do contato"),
    "cellphone": fields.String(description="Celular do contato"),
})

contact_rest_model_delete = server.api.model(
    'contact_rest_model_delete', {
    "id": fields.Integer(description="ID do contato", required=True)
})




