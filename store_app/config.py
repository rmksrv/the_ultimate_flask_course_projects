import pathlib


PROJECT_ROOT = pathlib.Path.cwd()


class AppConfig:
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = "some_secret_key"
    SQLALCHEMY_DATABASE_URI = r"sqlite:///store_app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = "images"
    UPLOADS_AUTOSERVE = True
