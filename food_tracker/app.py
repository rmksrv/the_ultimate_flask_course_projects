import datetime
import pathlib
import sqlite3

import dateutil.parser
import flask


DATABASE_PATH = pathlib.Path(__file__).parent / "food_tracker.db"
app = flask.Flask(__name__)


def new_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def db_connection() -> sqlite3.Connection:
    if not hasattr(flask.g, "sqlite_db"):
        flask.g.sqlite_db = new_db_connection()
    return flask.g.sqlite_db


@app.teardown_appcontext
def close_db(error) -> None:
    if hasattr(flask.g, "sqlite_db"):
        flask.g.sqlite_db.close()


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


@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        date_form_value = flask.request.form.get("date")
        if date_form_value:
            dt = dateutil.parser.parse(timestr=date_form_value).date()
        else:
            dt = datetime.date.today()
        add_log_date(dt)
    dates = [
        {
            "date": prettified_date(
                datetime.datetime.strptime(d["entry_date"], "%Y-%m-%d")
            ),
            "total": total_consumed_at_log_date(d["id"]),
        } for d in all_log_dates_ordered_by_desc()
    ]
    return flask.render_template("home.html", dates=dates)


@app.route("/view/<date>", methods=["GET", "POST"])
def view(date: str):
    entry_at = dateutil.parser.parse(date).date()
    log_date = log_date_by_entry_date(entry_at)
    log_date_id = log_date["id"]

    if flask.request.method == "POST":
        food_id = int(flask.request.form.get("food-select"))
        add_eating(food_id, log_date_id)

    parsed_date = dateutil.parser.parse(log_date["entry_date"])

    consumed_food_info = []
    for eating in eatings_by_log_date_id(log_date_id):
        consumed_food = food_by_id(eating["food_id"])
        consumed_food_info.append({
            "name": consumed_food["name"],
            "protein": consumed_food["protein"],
            "fat": consumed_food["fat"],
            "carbohydrates": consumed_food["carbohydrates"],
            "calories": consumed_food["calories"],
        })

    return flask.render_template(
        "day.html",
        date=prettified_date(parsed_date),
        foods=all_food(),
        consumed_food_info=consumed_food_info,
        total_consumed=total_consumed_at_log_date(log_date_id),
    )


@app.route("/food", methods=["GET", "POST"])
def food():
    if flask.request.method == "POST":
        name = flask.request.form.get("food-name")
        protein = int(flask.request.form.get("protein"))
        fat = int(flask.request.form.get("fat"))
        carbs = int(flask.request.form.get("carbohydrates"))
        calories = calories_from(protein, fat, carbs)
        add_food(name, protein, fat, carbs, calories)

    return flask.render_template("food.html", food_list=all_food())


def calories_from(
    protein: int,
    fat: int,
    carbs: int
) -> int:
    return 4 * protein + 4 * carbs + 9 * fat


def prettified_date(dt: datetime.date) -> str:
    return datetime.datetime.strftime(dt, "%B %d, %Y")


def total_consumed_at_log_date(log_date_id: int) -> dict[str, int]:
    total_consumed = {
        "protein": 0,
        "fat": 0,
        "carbohydrates": 0,
        "calories": 0,
    }
    for eating in eatings_by_log_date_id(log_date_id):
        consumed_food = food_by_id(eating["food_id"])
        total_consumed["protein"] += consumed_food["protein"]
        total_consumed["fat"] += consumed_food["fat"]
        total_consumed["carbohydrates"] += consumed_food["carbohydrates"]
        total_consumed["calories"] += consumed_food["calories"]
    return total_consumed


if __name__ == '__main__':
    app.run(debug=True)
