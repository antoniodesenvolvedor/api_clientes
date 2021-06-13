import pytest
import json
from base64 import b64encode
from src.server.server import server
from src.controllers import contacts_varejao
from tests.common_test_methods import  _test_if_method_is_checking_auth, \
    _test_code_for_non_existing_resource, _test_for_validation_of_payload, _test_success_code, _test_already_exists
import re

app = server.app

@pytest.fixture(scope="module")
def server_fix():
    return app.test_client()


@pytest.fixture(scope="module")
def header_basic_auth_fix():
    credentials = b64encode(str.encode("%s:%s" % ('usuarioteste@teste.com', 'secure_password'))). \
        decode('utf-8')
    return {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json"
    }


@pytest.fixture(scope="class")
def testing_user_fix(server_fix, header_basic_auth_fix):
    testing_user = {
        "email": 'usuarioteste@teste.com',
        "password": 'secure_password',
        "name": "Usuario de testes"
    }

    server_fix.post('/varejao/user', json=testing_user)
    response = server_fix.get('/varejao/user', json=testing_user, headers=header_basic_auth_fix)
    response = json.loads(response.data)
    token = response.get('token')
    testing_user['token'] = token

    return testing_user


class TestUser:

    url = '/varejao/user'
    def _test_get(self, test_server, test_header_basic_auth, test_user):
        response = test_server.get(self.url,  json={"email": "email_inexistente##@@@"})
        _test_if_method_is_checking_auth(response)

        response = test_server.get(self.url, headers=test_header_basic_auth)
        _test_for_validation_of_payload(response)

        response = test_server.get(self.url, headers=test_header_basic_auth, json={"email": "email_inexistente##@@@"})
        _test_if_method_is_checking_auth(response)

        response = test_server.get(self.url, headers=test_header_basic_auth,  json=test_user)
        response = json.loads(response.data)
        response_token = response.get('token')
        assert response_token == test_user['token']

    def _test_post(self, test_server):
        testing_user_2 = {
            "email": 'usuarioteste@teste.com_2',
            "password": 'secure_password',
        }

        credentials_2 = b64encode(str.encode("%s:%s" % (testing_user_2['email'], testing_user_2['password']))). \
            decode('utf-8')
        credentials_2 = {
            "Authorization": f"Basic {credentials_2}",
            "Content-Type": "application/json"
        }

        test_server.delete(self.url, headers=credentials_2, json=testing_user_2)

        response = test_server.post(self.url, json=testing_user_2)
        _test_for_validation_of_payload(response)

        testing_user_2['name'] = "Usuario de testes"
        response = test_server.post(self.url, json=testing_user_2)
        _test_success_code(response)

        response = test_server.post(self.url, json=testing_user_2)
        _test_already_exists(response)


    def _test_put(self, test_server, test_header_basic_auth, test_user):
        
        response = test_server.put(self.url, json=test_user)
        _test_if_method_is_checking_auth(response)

        response = test_server.put(self.url, headers=test_header_basic_auth)
        _test_for_validation_of_payload(response)

        response = test_server.put(self.url, json={"Wrong": "parameters"}, headers=test_header_basic_auth)
        _test_for_validation_of_payload(response)

        response = test_server.put(self.url, json=test_user, headers=test_header_basic_auth)
        _test_success_code(response)

    def _test_patch(self, test_server, test_header_basic_auth, test_user):

        response = test_server.patch(self.url, json=test_user)
        _test_if_method_is_checking_auth(response)

        response = test_server.patch(self.url, json={'email': 'Diferent email'}, headers=test_header_basic_auth)
        _test_if_method_is_checking_auth(response)

        response = test_server.patch(self.url, json=test_user, headers=test_header_basic_auth)
        _test_success_code(response)
        response_token = json.loads(response.data)
        assert response_token['token']




    def _test_delete(self, test_server, test_header_basic_auth, test_user):
        response = test_server.delete(self.url, json=test_user)
        _test_if_method_is_checking_auth(response)

        response = test_server.delete(self.url, json={'email': 'Diferent email'}, headers=test_header_basic_auth)
        _test_if_method_is_checking_auth(response)

        response = test_server.delete(self.url, json=test_user, headers=test_header_basic_auth)
        _test_success_code(response)

        response = test_server.delete(self.url, json=test_user, headers=test_header_basic_auth)
        _test_if_method_is_checking_auth(response)

    def test_user(self, server_fix, header_basic_auth_fix, testing_user_fix):
        self._test_get(server_fix, header_basic_auth_fix, testing_user_fix)
        self._test_post(server_fix)
        self._test_put(server_fix, header_basic_auth_fix, testing_user_fix)
        self._test_patch(server_fix, header_basic_auth_fix, testing_user_fix)
        self._test_delete(server_fix, header_basic_auth_fix, testing_user_fix)


@pytest.fixture(scope="class")
def testing_contact_list_fix():
    contact_list = {"contacts": [
        {
            "name": "Srta. Isabelly Castro",
            "cellphone": "5541959365078"
        },
        {
            "name": "Ana Julia da Rocha",
            "cellphone": "+55 (41) 96941-9199"
        }
    ]}

    return contact_list


@pytest.fixture(scope="class")
def testing_invalid_contact_list_fix():
    contact_list = {"contacts": [
        {
            "name": "Srta. Isabelly Castro",
            "cellphone": "5541959365078000000"
        },
        {
            "name": "Ana Julia da Rocha",
            "cellphone": "5419230380621"
        }
    ]}

    return contact_list


@pytest.fixture(scope="class")
def token_header_fix(testing_user_fix):
    return {
        'Token': testing_user_fix['token']
    }


class TestContact:

    url = '/varejao/contact'

    def _test_post(self, test_server, token_header, testing_contact_list, testing_invalid_contact_list):
        response = test_server.post(self.url, json=testing_contact_list)
        _test_if_method_is_checking_auth(response)

        response = test_server.post(self.url, headers=token_header, json=testing_invalid_contact_list)
        _test_for_validation_of_payload(response)

        response = test_server.post(self.url, json=testing_contact_list, headers=token_header)
        new_contacts = json.loads(response.data)

        for index, payload_contact in enumerate(testing_contact_list['contacts']):
            assert payload_contact['name'] == new_contacts[index]['name']
            assert re.sub("[^0-9]", "", payload_contact['cellphone']) == new_contacts[index]['cellphone']

        return new_contacts[0]


    def _test_get(self, test_server, token_header, new_contact):

        response = test_server.get(self.url)
        _test_if_method_is_checking_auth(response)

        response = test_server.get(self.url, headers=token_header)
        _test_success_code(response)
        response = json.loads(response.data)
        assert len(response['contacts']) > 0

        response = test_server.get(self.url + f'?id={new_contact["id"]}', headers=token_header)
        _test_success_code(response)

        response = json.loads(response.data)
        new_contact_response = response['contacts'][0]
        assert new_contact_response['id'] == new_contact["id"]
        assert new_contact_response['name'] == new_contact["name"]
        assert new_contact_response['cellphone'] == new_contact["cellphone"]

        response = test_server.get(self.url + f'?id=-9999999', headers=token_header)
        _test_code_for_non_existing_resource(response)

    def _test_delete(self, server_fix, token_header, new_contact):
        response = server_fix.delete(self.url, json=new_contact)
        _test_if_method_is_checking_auth(response)

        response = server_fix.delete(self.url, json={"id": -9999}, headers=token_header)
        _test_code_for_non_existing_resource(response)

        response = server_fix.delete(self.url, headers=token_header)
        _test_for_validation_of_payload(response)

        response = server_fix.delete(self.url, json=new_contact, headers=token_header)
        _test_success_code(response)

        response = server_fix.delete(self.url, json=new_contact, headers=token_header)
        _test_code_for_non_existing_resource(response)

    def _test_put(self, server_fix, token_header, new_contact):
        response = server_fix.put(self.url, json=new_contact)
        _test_if_method_is_checking_auth(response)

        response = server_fix.put(self.url, headers=token_header)
        _test_for_validation_of_payload(response)

        response = server_fix.put(self.url, json={"Wrong": "parameters"}, headers=token_header)
        _test_for_validation_of_payload(response)

        response = server_fix.put(self.url, json={"id": -9999}, headers=token_header)
        _test_code_for_non_existing_resource(response)

        novos_dados = {
            "cellphone": "554196rrrrrrrrr9419199",
            "name": "Jose",
            "id": new_contact["id"]
        }

        response = server_fix.put(self.url, json=novos_dados, headers=token_header)
        _test_success_code(response)

        response = server_fix.get(self.url + f'?id={new_contact["id"]}', headers=token_header)
        _test_success_code(response)

        response = json.loads(response.data)
        updated_contact_response = response['contacts'][0]

        novos_dados['cellphone'] = contacts_varejao.Contacts._format_cellphone_varejao(novos_dados['cellphone'])
        assert novos_dados['id'] == updated_contact_response["id"]
        assert novos_dados['name'] == updated_contact_response["name"]
        assert novos_dados['cellphone'] == updated_contact_response["cellphone"]


    def test_contact(self, server_fix, token_header_fix, testing_contact_list_fix, testing_invalid_contact_list_fix):
        new_contact = self._test_post(server_fix, token_header_fix, testing_contact_list_fix, testing_invalid_contact_list_fix)
        self._test_get(server_fix, token_header_fix, new_contact)
        self._test_put(server_fix, token_header_fix, new_contact)
        self._test_delete(server_fix, token_header_fix, new_contact)



