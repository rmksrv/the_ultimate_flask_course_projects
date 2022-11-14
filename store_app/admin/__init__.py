import flask

from admin import constants


admin_blueprint = flask.Blueprint(
    constants.APP_NAME,
    __name__,
    template_folder=constants.TEMPLATES_PATH,
    static_folder=constants.STATIC_PATH,
    url_prefix=constants.URL_PREFIX,
)

from admin import views
