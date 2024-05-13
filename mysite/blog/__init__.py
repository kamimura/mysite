from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

from mysite.db import get_db

from . import auth

bp = Blueprint(
    'blog',
    __name__,
    url_prefix='/blog',
    template_folder='templates',
    static_folder='static',
)
bp.register_blueprint(auth.bp)
bp.add_url_rule('/', endpoint='index')


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        """
select p.id, title, body, created, author_id, username
from post p join user u on p.author_id = u.id
order by created desc
"""
    ).fetchall()
    return render_template('blog/index.html.j2', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        if not title:
            error = "題名を入力してください。"
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                """
insert into post (title, body, author_id) values (?, ?, ?)
""",
                (title, body, g.user['id']),
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html.j2')


def get_post(id, check_author=True):
    post = (
        get_db()
        .execute(
            """
select p.id, title, body, created, author_id, username
from post p join user u on p.author_id = u.id
where p.id = ?
""",
            (id,),
        )
        .fetchone()
    )
    if post is None:
        abort(404, f"投稿 id {id}はありません。")
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@auth.login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        title = request.form['title']
        error = None
        if not title:
            error = '題名を入力してください。'
        if error is not None:
            flash(error)
        else:
            body = request.form['body']
            db = get_db()
            db.execute(
                """
update post set title = ?, body = ? where id = ?
""",
                (title, body, id),
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html.j2', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute(
        """
delete from post where id = ?
""",
        (id,),
    )
    db.commit()
    return redirect(url_for('blog.index'))
