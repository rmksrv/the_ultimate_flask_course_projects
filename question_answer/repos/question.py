from typing import Any

import database
import models
import repos.queries


def one_of(**params) -> models.Question | None:
    """
    Get models.Question object from database by "specifiers" params

    Arguments:
        **params: specifiers, if it needs to perform data filtering
    """
    specifiers = " ".join(params.keys())
    table_fields = [
        field for field in vars(models.Question).get("__annotations__")
        if not field.startswith("_")
    ]
    query = repos.queries.select_query(
        table_name=models.Question._table_name,
        table_fields=table_fields,
        specifiers=specifiers,
    )
    with database.Connection() as db:
        if params.values():
            param_list = [p for p in params.values()]
            question_record = db.connection.execute(query, param_list).fetchone()
        else:
            question_record = db.connection.execute(query).fetchone()
    if not question_record:
        return None
    return models.Question.from_dict(question_record)


def all_of(**params) -> list[models.Question]:
    """
    Get models.Question objects from database by "specifiers" params

    Arguments:
        **params: specifiers, if it needs to perform data filtering
    """
    specifiers = " ".join(params.keys())
    table_fields = [
        field for field in vars(models.Question).get("__annotations__")
        if not field.startswith("_")
    ]
    query = repos.queries.select_query(
        table_name=models.Question._table_name,
        table_fields=table_fields,
        specifiers=specifiers,
    )
    with database.Connection() as db:
        if params.values():
            param_list = [p for p in params.values()]
            question_records = db.connection.execute(query, param_list).fetchall()
        else:
            question_records = db.connection.execute(query).fetchall()
    return [models.Question.from_dict(record) for record in question_records]


def new(
    question: str,
    asking_user: models.User | None = None,
    asking_user_id: int | None = None,
    expert: models.User | None = None,
    expert_id: int | None = None,
    answer: str | None = None,
) -> models.Question:
    """
    Creates and returns new question

    Arguments:
        question: text of question
        asking_user: user asking. Excludes asking_user_id
        asking_user_id: user's asking. Excludes asking_user
        expert: answering user. Excludes expert_id
        expert_id: answering user. Excludes expert
        answer: text of answer
    """
    if not (asking_user or asking_user_id):
        raise ValueError("Neither 'asking_user' was provided, nor 'asking_user_id'")
    if not (expert or expert_id):
        raise ValueError("Neither 'expert' was provided, nor 'expert_id'")

    table_fields = [
        field for field in vars(models.Question).get("__annotations__")
        if not field.startswith("_") and not field == "id"
    ]
    query = repos.queries.insert_query(
        table_name=models.Question._table_name,
        table_fields=table_fields,
    )
    asking_user_id = asking_user_id or asking_user.id
    expert_id = expert_id or expert.id
    with database.Connection() as db:
        db.cursor.execute(query, [question, asking_user_id, expert_id, answer])
        db.connection.commit()
        new_question_id = db.cursor.lastrowid
    return models.Question(
        id=new_question_id,
        question=question,
        asking_user_id=asking_user_id,
        expert_id=expert_id,
        answer=answer,
    )


def change(
    updating_data: dict[str, Any],
    question: models.Question | None = None,
    **where_params,
) -> None:
    """
    Updates users of provided users of by where_params

    Arguments
        updating_data: dictionary with field and val to update
        question: if you have Question object, and you need to
                change it, you can pass this obj with this arg
        **where_params: WHERE conditions
    """
    table_fields = [
        field for field in vars(models.Question).get("__annotations__")
        if not field.startswith("_")
    ]
    specifiers = None
    params = None
    if question:
        specifiers = "id"
        params = [question.id]
    elif where_params:
        specifiers = " ".join(where_params.keys())
        params = [val for val in where_params.values()]
    query = repos.queries.update_query(
        table_name=models.Question._table_name,
        table_fields=table_fields,
        updating_data=updating_data,
        specifiers=specifiers
    )
    with database.Connection() as db:
        if specifiers:
            db.cursor.execute(query, params)
        else:
            db.cursor.execute(query)
        db.connection.commit()


def all_unanswered_questions(expert_id: int) -> list[models.Question]:
    query = "SELECT * FROM questions WHERE expert_id = ? AND answer IS NULL;"
    with database.Connection() as db:
        questions = db.cursor.execute(query, [expert_id]).fetchall()
    return [models.Question.from_dict(question) for question in questions]


def all_answered_questions() -> list[models.Question]:
    query = "SELECT * FROM questions WHERE answer IS NOT NULL;"
    with database.Connection() as db:
        questions = db.cursor.execute(query).fetchall()
    return [models.Question.from_dict(question) for question in questions]
