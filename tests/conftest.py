import os
import tempfile

import pytest
from flask import Flask

from mysite import create_app
from mysite.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'blog', 'data.sql')) as f:
    _data_sql = f.read()


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app(
        {'TESTING': True, 'DATABASE': db_path, 'WTF_CSRF_ENABLED': False}
    )
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def runner(app: Flask):
    return app.test_cli_runner()
