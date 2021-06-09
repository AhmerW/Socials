import requests
import pytest

API_URL = 'http://localhost:8000'

class TestUser:
    username = 'test'
    password = 'pass'


@pytest.mark.skip()
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