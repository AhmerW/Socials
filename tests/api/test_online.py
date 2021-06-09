from tests.client import Client

client = Client()

def test_api_online():
    assert client.request('get', '/').status_code == 200