from flask import Blueprint
from .views import login

auth_blueprint = Blueprint('auth', __name__)

auth_blueprint.add_url_rule('/auth/login/', view_func=login, methods=['POST'])
