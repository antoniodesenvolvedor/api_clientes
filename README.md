# api_clientes
API responsável por manter contatos de dois clientes macapa e varejao

Ambos os serviços dos clientes permitem excluir, atualizar, cadastrar, atualizar e listar os contatos 
É possível acessar a documentação swagger no endereço /docs. A API está configurada para escutar na porta 5001,
mas essa e outras configurações podem ser alteradas no arquivo .env


## Tecnologias

- Python 3:8
- Flask
- PyJWT
- PostgreSql
- Redis
- flask_restplus
- ORM SQLAlchemy
- Pytest
- Docker
- Mysql
- docker-compose 3.9

## Iniciando a aplicação com Docker
git clone  https://github.com/antoniodesenvolvedor/api_clientes.git 

docker-compose up -d

Os bancos de dados já serão criados com o ORM, incluindo as tabelas. Para fazer
requisições é necessário primeiro cadastrar um token.

Na rotas a seguir é possível cadastrar um usuário, faça o cadastro com a seguinte payload

POST
/macapa/user
/varejao/user

{
  "email": "string",
  "password": "string",
  "name": "string"
}

Após, acessas uma das rotas a seguir para obter o token, é necessário utilizar basic
auth com o e-mail e senha criado anteriormente, informar o mesmo e-mail no corpo da requisição

GET
/macapa/user
/macapa/user
{
  "email": "string"
}

Será retornado um token, esse token deve ser utilizado no header de toda a requisição
em /macapa/contact e /varejao/contact.

É possível alterar o token, para mais informações acesse a rota /docs no navegador

###### Por motivo de testes, foi disponibilizado no repositório um .env. Mas em cenários reais deixar o .env no repositório é uma má prática.


## Preparando o ambiente de desenvolvimento

Para rodar a aplicação localmente é só alterar a variável PRODUCTION para 0 no arquivo .env e 
executar o arquivo main.py, é necessário subir o Redis, Mysql e Postgres, pode-se utilizar 
o próprio docker-compose do projeto, porém, ao rodar a aplicação localmente é necessário 
ou alterar a porta da aplicação, ou parar o serviço correspondente se foi subido com docker-compose.

## Testes
O código  foi amplamenta coberto com testes automátizados, basta acessar a pasta raiz do projeto com o terminal e digitar pytest e pressionar enter. 
Existem testes para ambos os clientes, para testar apenas um cliente entre com o comando

pytest ./tests/test_macapa.py
pytest ./tests/test_varejao.py


