import datetime

from flask import Blueprint, abort, redirect, render_template, request, url_for

from mysite.db import UseDataBase, get_db
from mysite.polls.db import (
    get_choices,
    get_question,
    increment_choice,
    was_published_recently,
)

bp = Blueprint(
    'polls',
    __name__,
    url_prefix='/polls',
    template_folder='templates',
    static_folder='static',
)
bp.add_url_rule('/', endpoint='index')


@bp.route('/')
def index():
    questions = (
        get_db()
        .execute(
            """
select * from polls_question order by pub_date desc
"""
        )
        .fetchall()
    )
    latest_question_list = [q for q in questions if was_published_recently(q)][
        :5
    ]
    return render_template(
        'polls/index.html.j2', latest_question_list=latest_question_list
    )


@bp.route('/<int:question_id>/detail')
def detail(question_id):
    question = get_question(question_id)
    if question is None:
        abort(404)
    if question['pub_date'] > datetime.datetime.now():
        abort(404)
    choices = get_choices(question_id)
    return render_template(
        'polls/detail.html.j2', question=question, choices=choices
    )


@bp.route('/<int:question_id>/results')
def results(question_id: int):
    return render_template(
        'polls/results.html.j2',
        question=get_question(question_id),
        choices=get_choices(question_id),
    )


@bp.route('/<int:question_id>/vote', methods=('POST',))
def vote(question_id):
    question = get_question(question_id)
    if question is None:
        abort(404)
    selected_choice_id = int(request.form['choice'])
    if selected_choice_id is None:
        pass
    with UseDataBase() as cur:
        choice = cur.execute(
            """
select * from polls_choice where id = ?
""",
            (selected_choice_id,),
        ).fetchone()
    increment_choice(choice_id=choice['id'])
    return redirect(url_for('polls.results', question_id=question_id))
