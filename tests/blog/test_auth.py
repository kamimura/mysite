import pytest
from flask import Flask, g, session, testing

from mysite.db import get_db


def test_register(client: testing.FlaskClient, app: Flask):
    assert client.get('/blog/auth/register').status_code == 200
    res = client.post(
        '/blog/auth/register', data={'username': 'a', 'password': 'a'}
    )
    assert res.status_code == 302
    assert res.headers['Location'] == '/blog/auth/login'
    with app.app_context():
        assert (
            get_db()
            .execute("select * from user where username = 'a'")
            .fetchone
            is not None
        )


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (('test', 'test', '既に使われています。'),),
)
def test_register_validate_input(
    client: testing.FlaskClient, username, password, message
):
    res = client.post(
        '/blog/auth/register',
        data={'username': username, 'password': password},
    )
    assert message.encode('utf8') in res.data


def test_login(client: testing.FlaskClient, auth):
    assert client.get('/blog/auth/login').status_code == 200
    res = auth.login()
    assert res.headers['Location'] == '/blog/'
    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
        ('a', 'test', '登録されてません'),
        ('test', 'a', 'パスワードが違います。'),
    ),
)
def test_login_valiate_input(auth, username, password, message):
    res = auth.login(username, password)
    assert message in res.data.decode('utf8')


def test_logout(auth, client):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session
