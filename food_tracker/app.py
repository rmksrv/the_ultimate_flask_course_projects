import datetime
import dateutil.parser
import flask

import database

app = flask.Flask(__name__)


@app.teardown_appcontext
def close_db(error) -> None:
    if hasattr(flask.g, "sqlite_db"):
        flask.g.sqlite_db.close()


@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        date_form_value = flask.request.form.get("date")
        if date_form_value:
            dt = dateutil.parser.parse(timestr=date_form_value).date()
        else:
            dt = datetime.date.today()
        database.add_log_date(dt)
    dates = [
        {
            "date": prettified_date(
                datetime.datetime.strptime(d["entry_date"], "%Y-%m-%d")
            ),
            "total": total_consumed_at_log_date(d["id"]),
        } for d in database.all_log_dates_ordered_by_desc()
    ]
    return flask.render_template("home.html", title="Home", dates=dates)


@app.route("/view/<date>", methods=["GET", "POST"])
def view(date: str):
    entry_at = dateutil.parser.parse(date).date()
    log_date = database.log_date_by_entry_date(entry_at)
    log_date_id = log_date["id"]

    if flask.request.method == "POST":
        food_id = int(flask.request.form.get("food-select"))
        database.add_eating(food_id, log_date_id)

    parsed_date = dateutil.parser.parse(log_date["entry_date"])

    consumed_food_info = []
    for eating in database.eatings_by_log_date_id(log_date_id):
        consumed_food = database.food_by_id(eating["food_id"])
        consumed_food_info.append({
            "name": consumed_food["name"],
            "protein": consumed_food["protein"],
            "fat": consumed_food["fat"],
            "carbohydrates": consumed_food["carbohydrates"],
            "calories": consumed_food["calories"],
        })
    pretty_date = prettified_date(parsed_date)
    return flask.render_template(
        "day.html",
        title=pretty_date,
        date=pretty_date,
        foods=database.all_food(),
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
        database.add_food(name, protein, fat, carbs, calories)

    return flask.render_template(
        "food.html",
        title="Add food",
        food_list=database.all_food(),
    )


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
    for eating in database.eatings_by_log_date_id(log_date_id):
        consumed_food = database.food_by_id(eating["food_id"])
        total_consumed["protein"] += consumed_food["protein"]
        total_consumed["fat"] += consumed_food["fat"]
        total_consumed["carbohydrates"] += consumed_food["carbohydrates"]
        total_consumed["calories"] += consumed_food["calories"]
    return total_consumed


if __name__ == '__main__':
    app.run(debug=True)
