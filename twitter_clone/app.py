import datetime

import flask
import flask.cli
import flask_login
import flask_migrate
import flask_sqlalchemy
import flask_uploads

import constants


app = flask.Flask(__name__)
upload_photos_set = flask_uploads.UploadSet(
    "photos",
    flask_uploads.IMAGES,
)
app.config |= {
    "SECRET_KEY": constants.SECRET_KEY,
    "DEBUG": constants.DEBUG,
    "SQLALCHEMY_DATABASE_URI": constants.DATABASE_URI,
    "UPLOADS_AUTOSERVE": True,
    "UPLOADED_PHOTOS_DEST": str(constants.UPLOADED_IMAGES_PATH),
}
flask_uploads.configure_uploads(
    app,
    [
        upload_photos_set,
    ],
)
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)
login_manager = flask_login.LoginManager(app)
login_manager.login_view = "index"  # type: ignore
app_cli = flask.cli.FlaskGroup(app)  # type: ignore

import views


@app.template_filter("time_since")
def time_since(delta: datetime.timedelta) -> str:
    total_minutes, _ = divmod(delta.seconds, 60)
    hours, minutes = divmod(total_minutes, 60)
    if delta.days > 0:
        return f"{delta.days}d"
    elif hours > 0:
        return f"{hours}h"
    elif minutes > 0:
        return f"{minutes}m"
    return "Just now"


if __name__ == "__main__":
    app_cli()
