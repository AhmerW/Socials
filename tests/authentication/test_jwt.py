
from tests.client import Client, TestUser

client = Client()


def _base_test(json, url='/auth/token'):
    return client.request(
        'post',
        url,
        data=json
    )


def test_auth_jwt_bad_token():
    response = _base_test({'username': 'bad-username', 'password': 'bad-passwod'})
    assert response.json().get('ok') is False
    
def test_auth_jwt_correct_token():
    response = _base_test({'username': TestUser.username, 'password': TestUser.password})
    assert response.json().get('ok') is True
    