CREATE TABLE log_date(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_date DATE NOT NULL
);

CREATE TABLE food(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    protein INTEGER NOT NULL,
    fat INTEGER NOT NULL,
    carbohydrates INTEGER NOT NULL,
    calories INTEGER NOT NULL
);

CREATE TABLE eating(
    food_id INTEGER,
    log_date_id INTEGER,
    PRIMARY KEY(food_id, log_date_id)
);