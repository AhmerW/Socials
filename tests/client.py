import requests
import pytest

API_URL = 'http://localhost:8000'
INTERNAL_USERNAME_PREFIX = 'internal_test_user'


@pytest.mark.skip()
class Client(requests.Session):
    def __init__(self, base: str = API_URL):
        super().__init__()
        self._base = base

    def request(self, type_, path, *args, **kwargs):
        if not path.startswith('/'):
            path = f'/{path}'
        return super().request(
            type_,
            f'{self._base}{path}',
            *args, **kwargs
        )


def _format_token(token, as_header=False):
    if as_header:
        return {
            'Authorization': f'bearer {token}'
        }
    return token


@pytest.mark.skip()
class TestUser:
    username = 'admin'
    password = 'pass'

    __cached = {}

    @classmethod
    def auth(cls, client: Client, header=True):
        _existing = cls.__cached.get(cls.username)
        if _existing is not None:
            return _format_token(_existing, header)
        token = client.request(
            'post',
            '/auth/login',
            data={'username': cls.username,
                  'password': cls.password, 'device_id': 'tests'}
        ).json().get('data', dict()).get('access_token')
        cls.__cached[cls.username] = token
        return _format_token(token, header)
