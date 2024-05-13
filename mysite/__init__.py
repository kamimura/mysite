import os

from flask import Flask
from flask_wtf import CSRFProtect

from mysite import blog, db, polls

csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'mysite.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.mkdir(app.instance_path)
    except OSError as err:
        pass
    except Exception as err:
        print(err)
    db.init_app(app)
    csrf.init_app(app)
    app.register_blueprint(blog.bp)
    app.register_blueprint(polls.bp)

    @app.route('/')
    @app.route('/index')
    def index():
        return ''

    return app
