import logging
from logging import Formatter
from celery import Celery
from flask import Flask
from flask.logging import default_handler

from config import config_modes, BaseConfig
from extensions import db, mi, jwt


# this instance is to be used only to decorate functions as tasks
celery_instance = Celery(
        __name__,
        backend=BaseConfig.CELERY_RESULT_BACKEND,
        broker=BaseConfig.CELERY_BROKER_URL
    )


def create_app(config_name):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_modes[config_name])

    setup_logger(flask_app)
    register_endpoints(flask_app)
    setup_extensions(flask_app)

    return flask_app


def register_endpoints(flask_app):
    from app.api.base.views import unhandled_exception, internal_server_error, page_not_found
    from app.api.hello import hello_blueprint
    from app.api.users import users_blueprint

    flask_app.register_blueprint(hello_blueprint)
    flask_app.register_blueprint(users_blueprint)
    flask_app.register_error_handler(404, page_not_found)
    flask_app.register_error_handler(500, internal_server_error)
    flask_app.register_error_handler(Exception, unhandled_exception)


def setup_logger(app):
    formatter = Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s : %(lineno)d] :::: %(message)s'
    )
    default_handler.setFormatter(formatter)
    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        if gunicorn_logger.level:
            # When gunicorn_logger.level is greater than 0, it
            # means app was initialized through gunicorn.
            app.logger.handlers = gunicorn_logger.handlers
            app.logger.setLevel(gunicorn_logger.level)


def setup_extensions(app):
    db.init_app(app)
    mi.init_app(app, db)
    jwt.init_app(app)


# TODO Authorization
# TODO API to alter ClientToken revoke status
# TODO API to create new ClientToken for existing ClientUser
