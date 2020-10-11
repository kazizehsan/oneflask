from flask import Blueprint

from .views import instant_hello, celery_hello

hello_blueprint = Blueprint('api', __name__)


hello_blueprint.add_url_rule('/', 'hello', instant_hello, methods=['GET'])

hello_blueprint.add_url_rule('/celery/', 'celery_hello', celery_hello, methods=['POST'])
