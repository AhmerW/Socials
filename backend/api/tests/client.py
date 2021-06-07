import requests
import pytest

API_URL = 'http://localhost:8000'
TEST_USER = 'test'
TEST_PASSWD = 'pass'

@pytest.mark.skip(reason="Class not meant for testing")
class Client(requests.Session):
    def __init__(self, base : str = API_URL):
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