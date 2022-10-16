CREATE TABLE users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT NOT NULL,
    password TEXT NOT NULL,
    role     TEXT NOT NULL
);

CREATE TABLE questions (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    question       TEXT NOT NULL,
    answer         TEXT,
    asking_user_id INTEGER NOT NULL,
    expert_id      INTEGER NOT NULL,

    FOREIGN KEY (asking_user_id) REFERENCES users(id),
    FOREIGN KEY (expert_id) REFERENCES users(id)
);
