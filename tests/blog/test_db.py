import sqlite3

import pytest

from mysite.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    with pytest.raises(sqlite3.ProgrammingError) as err:
        db.execute('select 1')
    assert 'closed' in str(err.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('mysite.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert '初期化' in result.output
    assert Recorder.called
