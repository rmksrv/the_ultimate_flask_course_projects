import pathlib

import flask_uploads


APP_NAME = "admin"
PROJECT_ROOT = pathlib.Path.cwd().parent
APP_ROOT = PROJECT_ROOT / APP_NAME
TEMPLATES_PATH = "templates"
STATIC_PATH = "static"
URL_PREFIX = f"/{APP_NAME}"
UPLOAD_PHOTO_SET = flask_uploads.UploadSet("photos", flask_uploads.IMAGES)
