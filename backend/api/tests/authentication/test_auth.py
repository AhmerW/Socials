from client import Client

client = Client()


def _base_test(json, url='/auth/token'):
    return client.request(
        'post',
        url,
        data=json
    )


def test_auth_jwt_bad_token():
    response = _base_test({'username': 'bad-username', 'password': 'bad-passwod'})
    assert not response.json().get('ok') 
    
def test_auth_jwt_correct_token():
    response = _base_test({'username': 'test', 'password': 'pass'})
    assert response.json().get('ok')
    