import pytest
from flask import testing

from mysite.db import get_db


def test_index(client: testing.FlaskClient, auth):
    res = client.get('/blog/')
    assert 'ログイン' in res.data.decode('utf8')
    assert '登録' in res.data.decode('utf8')
    auth.login()
    res = client.get('/blog/')
    data = res.data.decode('utf8')
    assert 'ログアウト' in data
    assert 'test title' in data
    assert 'test\nbody' in data
    assert 'href="/blog/1/update' in data


@pytest.mark.parametrize('path', ('create', '1/update', '1/delete'))
def test_login_required(client: testing.FlaskClient, path: str):
    res = client.post(f'/blog/{path}')
    assert res.headers['Location'] == '/blog/auth/login'


def test_author_required(app, client, auth):
    with app.app_context():
        db = get_db()
        db.execute(
            """
update post set author_id = 2 where author_id = 1
"""
        )
        db.commit()
    auth.login()
    assert client.post('/blog/1/update').status_code == 403


@pytest.mark.parametrize('path', ('/2/update', '/2/delete'))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post('/blog{path}').status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/blog/create').status_code == 200
    client.post('/blog/create', data={'title': 'created', 'body': ''})
    with app.app_context():
        db = get_db()
        count = db.execute(
            """
select count (id) from post
"""
        ).fetchone()[0]
        assert count == 2


def test_update(auth, client, app):
    auth.login()
    assert client.get('/blog/1/update').status_code == 200
    client.post('/blog/1/update', data={'title': 'updated', 'body': ''})
    with app.app_context():
        db = get_db()
        post = db.execute('select * from post where id = 1').fetchone()
        assert post['title'] == 'updated'


@pytest.mark.parametrize('path', ('create', '1/update'))
def test_create_update_validate(client, auth, path):
    auth.login()
    res = client.post(f'/blog/{path}', data={'title': '', 'body': ''})
    assert '題名を入力してください' in res.data.decode('utf8')


def test_delete(auth, client, app):
    auth.login()
    res = client.post('/blog/1/delete')
    assert res.headers['Location'] == '/blog/'
    with app.app_context():
        db = get_db()
        post = db.execute('select * from post where id = 1').fetchone()
        assert post is None
