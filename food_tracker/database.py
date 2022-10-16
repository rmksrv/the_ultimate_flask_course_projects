import datetime
import pathlib
import sqlite3

import flask

DATABASE_PATH = pathlib.Path(__file__).parent / "food_tracker.db"


def new_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def db_connection() -> sqlite3.Connection:
    if not hasattr(flask.g, "sqlite_db"):
        flask.g.sqlite_db = new_db_connection()
    return flask.g.sqlite_db


def add_food(
    name: str,
    protein: int,
    fat: int,
    carbs: int,
    calories: int,
) -> None:
    db = db_connection()
    query = (
        "INSERT INTO food "
        "(name, protein, fat, carbohydrates, calories) "
        "VALUES (?, ?, ?, ?, ?)"
    )
    db.execute(query, [name, protein, fat, carbs, calories])
    db.commit()


def all_food() -> list[sqlite3.Row]:
    db = db_connection()
    query = "SELECT * FROM food"
    food_list = db.execute(query).fetchall()
    return food_list


def food_by_id(id: int) -> sqlite3.Row | None:
    db = db_connection()
    query = "SELECT * FROM food WHERE id = ?"
    f = db.execute(query, [id]).fetchone()
    return f


def add_log_date(d: datetime.date) -> None:
    db = db_connection()
    query = "INSERT INTO log_date (entry_date) VALUES (?)"
    db.execute(query, [d])
    db.commit()


def all_log_dates_ordered_by_desc() -> list[sqlite3.Row]:
    db = db_connection()
    query = "SELECT * FROM log_date ORDER BY entry_date DESC"
    date_list = db.execute(query).fetchall()
    return date_list


def log_date_by_entry_date(entry_date: datetime.date) -> sqlite3.Row | None:
    db = db_connection()
    query = "SELECT * FROM log_date WHERE entry_date = ?"
    d = (
        db.execute(query, [entry_date])
        .fetchone()
    )
    return d


def log_date_by_id(id: int) -> sqlite3.Row | None:
    db = db_connection()
    query = "SELECT * FROM log_date WHERE id = ?"
    d = (
        db.execute(query, [id])
        .fetchone()
    )
    return d


def add_eating(food_id: int, log_date_id: int) -> None:
    db = db_connection()
    query = "INSERT INTO eating VALUES (?, ?)"
    db.execute(query, [food_id, log_date_id])
    db.commit()


def all_eatings() -> list[sqlite3.Row]:
    db = db_connection()
    query = "SELECT * FROM eating"
    eating_list = db.execute(query).fetchall()
    return eating_list


def eatings_by_log_date_id(log_date_id: int) -> list[sqlite3.Row]:
    db = db_connection()
    query = "SELECT * FROM eating WHERE log_date_id = ?"
    eatings_list = db.execute(query, [log_date_id]).fetchall()
    return eatings_list

