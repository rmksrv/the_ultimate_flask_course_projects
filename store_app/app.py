import flask
import flask_uploads


def make_app() -> tuple[flask.Flask, flask.cli.FlaskGroup]:
    app = flask.Flask(__name__)
    app.config.from_object("config.AppConfig")
    configure_db(app)
    configure_uploads(app)
    register_blueprints(app)
    register_error_handlers(app)
    configure_logging(app)
    cli = flask.cli.FlaskGroup(app)  # type: ignore
    return app, cli


def configure_uploads(app: flask.Flask) -> None:
    import admin.constants

    upload_sets = [
        admin.constants.UPLOAD_PHOTO_SET,
    ]
    flask_uploads.configure_uploads(app, upload_sets)


def configure_db(app: flask.Flask) -> None:
    import store.models

    store.models.db.init_app(app)

    with app.app_context():
        if store.models.db.engine.url.drivername == "sqlite":
            store.models.migrate.init_app(
                app, store.models.db, render_as_batch=True
            )
        else:
            store.models.migrate.init_app(app, store.models.db)


def register_blueprints(app: flask.Flask) -> None:
    from admin import admin_blueprint
    from store import store_blueprint

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(store_blueprint)


def register_error_handlers(app: flask.Flask) -> None:
    pass


def configure_logging(app: flask.Flask) -> None:
    pass


app, cli = make_app()


if __name__ == "__main__":
    cli()
