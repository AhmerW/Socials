import secrets

from tests.client import Client, TestUser, INTERNAL_USERNAME_PREFIX


client = Client()


def test_register():
    response = client.request(
        'post',
        '/account/new',
        headers={'Base': TestUser.auth(client, False)},
        json={
            'username': f'{INTERNAL_USERNAME_PREFIX}{secrets.token_urlsafe(2)}',
            'password': 'password'
        }
    )
    print(response.text)
    #assert response.get('status') == 202
