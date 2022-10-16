from typing import Any, Iterable

import database
import models
import repos.queries


def one_of(**params) -> models.User | None:
    """
    Get models.User object from database by "specifiers" params

    Arguments:
        **params: specifiers, if it needs to perform data filtering
    """
    specifiers = " ".join(params.keys())
    table_fields = [
        field for field in vars(models.User).get("__annotations__")
        if not field.startswith("_")
    ]
    query = repos.queries.select_query(
        table_name=models.User._table_name,
        table_fields=table_fields,
        specifiers=specifiers,
    )
    with database.Connection() as db:
        if params.values():
            param_list = [p for p in params.values()]
            user_record = db.connection.execute(query, param_list).fetchone()
        else:
            user_record = db.connection.execute(query).fetchone()
    if not user_record:
        return None
    return models.User.from_dict(user_record)


def all_of(**params) -> list[models.User]:
    """
    Get models.User objects from database by "specifiers" params

    Arguments:
        **params: specifiers, if it needs to perform data filtering
    """
    specifiers = " ".join(params.keys())
    table_fields = [
        field for field in vars(models.User).get("__annotations__")
        if not field.startswith("_")
    ]
    query = repos.queries.select_query(
        table_name=models.User._table_name,
        table_fields=table_fields,
        specifiers=specifiers,
    )
    with database.Connection() as db:
        if params.values():
            param_list = [p for p in params.values()]
            user_records = db.connection.execute(query, param_list).fetchall()
        else:
            user_records = db.connection.execute(query).fetchall()
    return [models.User.from_dict(record) for record in user_records]


def new(name: str, password: str, role: models.UserRole) -> models.User:
    """
    Creates and returns new user

    Arguments:
        name: user's name
        password: user's password
        role: user's role
    """
    table_fields = [
        field for field in vars(models.User).get("__annotations__")
        if not field.startswith("_") and not field == "id"
    ]
    query = repos.queries.insert_query(
        table_name=models.User._table_name,
        table_fields=table_fields,
    )
    with database.Connection() as db:
        db.cursor.execute(query, [name, password, role])
        db.connection.commit()
        new_user_id = db.cursor.lastrowid
    return models.User(
        id=new_user_id,
        name=name,
        password=password,
        role=role
    )


def change(
    updating_data: dict[str, Any],
    user: models.User | None = None,
    **where_params,
) -> None:
    """
    Updates users of provided users of by where_params

    Arguments
        updating_data: dictionary with field and val to update
        user: if you have User object, and you need to
                change it, you can pass this obj with this arg
        **where_params: WHERE conditions
    """
    table_fields = [
        field for field in vars(models.User).get("__annotations__")
        if not field.startswith("_")
    ]
    specifiers = None
    params = None
    if user:
        specifiers = "id"
        params = [user.id]
    elif where_params:
        specifiers = " ".join(where_params.keys())
        params = [val for val in where_params.values()]
    query = repos.queries.update_query(
        table_name=models.User._table_name,
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
