import pathlib
import sqlite3


DATABASE_PATH = pathlib.Path(__file__).parent / "questions.db"


class Connection:

    def __init__(self, path: pathlib.Path = DATABASE_PATH):
        self.path = path

    def __enter__(self):
        self.connection: sqlite3.Connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.cursor: sqlite3.Cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
