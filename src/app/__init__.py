import logging
import traceback
from celery import Celery
from flask import (
    Flask,
    jsonify, make_response, request,
)

from config import config_modes, BaseConfig
from extensions import db, mi


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


def register_endpoints(app):

    from app.api.hello import hello_blueprint

    app.register_blueprint(hello_blueprint)

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        traceback.print_exc()
        return jsonify(
            data={'success': False},
            errors={'message': str(e)}
        ), 500

    @app.errorhandler(404)
    def page_not_found(error):
        app.logger.error('Page not found: %s', request.path)
        return make_response(jsonify({
            'message': f'{str(error)}'
        })), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error('Server Error: %s', error)
        return make_response(jsonify({
            'message': f'{str(error)}'
        })), 500


def setup_logger(app):
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