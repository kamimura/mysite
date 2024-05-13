import pytest
from flask.testing import FlaskClient


class AuthActions:
    def __init__(self, client: FlaskClient):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/blog/auth/login',
            data={'username': username, 'password': password},
        )

    def logout(self):
        return self._client.get('/blog/auth/logout')


@pytest.fixture
def auth(client: FlaskClient):
    return AuthActions(client)
