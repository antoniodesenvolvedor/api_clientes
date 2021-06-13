def _test_for_internal_server_error(response):
    assert response.status_code == 500

def _test_if_method_is_checking_auth(response):
    assert response.status_code == 401

def _test_code_for_non_existing_resource(response):
    assert response.status_code == 404

def _test_for_validation_of_payload(response):
    assert response.status_code == 400

def _test_success_code(response):
    assert response.status_code in (200, 201)


def _test_already_exists(response):
    assert response.status_code == 202
