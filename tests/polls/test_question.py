import datetime

from mysite.polls.db import (
    create_question,
    delete_all_question,
    was_published_recently,
)


def test_was_published_recently_with_future_question():
    t = datetime.datetime.now() + datetime.timedelta(days=1)
    future_question = {'pub_date': t}
    assert not was_published_recently(future_question)


def test_was_published_recently_with_old_question():
    old_question = {
        'pub_date': datetime.datetime.now()
        - datetime.timedelta(days=1, seconds=1)
    }
    assert not was_published_recently(old_question)


def test_was_published_recently_with_recent_quesiton():
    recent_question = {
        'pub_date': datetime.datetime.now()
        - datetime.timedelta(hours=23, minutes=59)
    }
    assert was_published_recently(recent_question)


def test_no_question(app, client):
    with app.app_context():
        delete_all_question()
        res = client.get('/polls/')
        assert res.status_code == 200
        assert "まだ調査はありません。" in res.data.decode('utf8')


def test_past_question(app, client):
    with app.app_context():
        delete_all_question()
        create_question('test1', days=-1)
        res = client.get('/polls/')
        assert res.status_code == 200
        assert "まだ調査はありません。" in res.get_data(as_text=True)


def test_future_question(app, client):
    with app.app_context():
        delete_all_question()
        create_question('test1', days=1)
        res = client.get('/polls/')
        assert res.status_code == 200
        assert "まだ調査はありません。" in res.get_data(as_text=True)


def test_past_and_future_question(app, client):
    with app.app_context():
        delete_all_question()
        create_question('test1', days=-1)
        create_question('test1', days=1)
        res = client.get('/polls/')
        assert res.status_code == 200
        assert "まだ調査はありません。" in res.get_data(as_text=True)


def test_two_past_question(app, client):
    with app.app_context():
        delete_all_question()
        create_question('test1', days=2)
        create_question('test1', days=1)
        res = client.get('/polls/')
        assert res.status_code == 200
        assert "まだ調査はありません。" in res.get_data(as_text=True)


def test_recent_question(app, client):
    with app.app_context():
        delete_all_question()
        create_question('test1')
        res = client.get('/polls/')
        assert res.status_code == 200
        assert res.get_data(as_text=True).count('<li>') == 1


def test_two_recent_question(app, client):
    with app.app_context():
        delete_all_question()
        create_question('test1')
        create_question('test2')
        res = client.get('/polls/')
        assert res.status_code == 200
        assert res.get_data(as_text=True).count('<li>') == 2


def test_detail_future(app, client):
    with app.app_context():
        delete_all_question()
        create_question('test', days=1)
        res = client.get('/polls/3/detail')
        assert res.status_code == 404


def test_detail_past(app, client):
    with app.app_context():
        delete_all_question()
        question = create_question('past question detail', days=-30)
        res = client.get('/polls/3/detail')
        assert res.status_code == 200
        assert 'past question detail' in res.get_data(as_text=True)
