import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from mysite.db import get_db

bp = Blueprint(
    'auth', __name__, url_prefix='/auth', template_folder='templates/blog/auth'
)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        try:
            db.execute(
                "insert into user (username, password) values (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
        except Exception:
            error = f'ユーザー名「{username}」は既に使われています。'
        else:
            return redirect(url_for('blog.auth.login'))
        flash(error)
    return render_template('register.html.j2')


@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        db = get_db()
        user = db.execute(
            "select * from user where username = ?", (username,)
        ).fetchone()
        if user is None:
            error = f"ユーザー名「{username}」は登録されてません。"
        elif not check_password_hash(user['password'], password):
            error = "パスワードが違います。"
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('blog.index'))
        flash(error)
    return render_template('login.html.j2')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db()
            .execute("select * from user where id = ?", (user_id,))
            .fetchone()
        )


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))


def login_required(func):
    @functools.wraps(func)
    def wrap(**kwargs):
        if g.user is None:
            return redirect(url_for('blog.auth.login'))
        return func(**kwargs)

    return wrap
