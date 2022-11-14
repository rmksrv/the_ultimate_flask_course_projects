import flask

from store import constants


store_blueprint = flask.Blueprint(
    constants.APP_NAME,
    __name__,
    template_folder=constants.TEMPLATES_PATH,
    static_folder=constants.STATIC_PATH,
)

from store import views
