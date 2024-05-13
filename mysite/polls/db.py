import datetime

from mysite.db import UseDataBase


def get_question(question_id):
    with UseDataBase() as cur:
        question = cur.execute(
            """
select * from polls_question where id = ?""",
            (question_id,),
        ).fetchone()
    return question


def get_choices(question_id):
    with UseDataBase() as cur:
        choices = cur.execute(
            """
select * from polls_choice where question_id = ?""",
            (question_id,),
        ).fetchall()
    return choices


def increment_choice(choice_id):
    with UseDataBase() as cur:
        cur.execute(
            """
update polls_choice set votes = votes + 1 where id = ?
""",
            (choice_id,),
        )


def was_published_recently(question):
    return (
        datetime.datetime.now() - datetime.timedelta(days=1)
        <= question['pub_date']
        <= datetime.datetime.now()
    )


def create_question(question_text, days=0):
    t = datetime.datetime.now() + datetime.timedelta(days=days)
    with UseDataBase() as cur:
        cur.execute(
            """
insert into polls_question (question_text, pub_date) values (?, ?)
""",
            (question_text, str(t)),
        )
    return {'question_text': question_text, 'pub_date': str(t)}


def delete_all_question():
    with UseDataBase() as cur:
        cur.execute(
            """
delete from polls_question
"""
        )
