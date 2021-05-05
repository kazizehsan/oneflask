from flask import Blueprint
from . import models
from .views import create_user_by_self, create_user_by_admin, list_users, get_me, get_user, update_me, update_user_by_admin, delete_user

users_blueprint = Blueprint('users', __name__)

users_blueprint.add_url_rule('/users/', view_func=create_user_by_admin, methods=['POST'])
users_blueprint.add_url_rule('/users/signup/', view_func=create_user_by_self, methods=['POST'])
users_blueprint.add_url_rule('/users/', view_func=list_users, methods=['GET'])
users_blueprint.add_url_rule('/users/me/', view_func=get_me, methods=['GET'])
users_blueprint.add_url_rule('/users/me/', view_func=update_me, methods=['PUT'])
users_blueprint.add_url_rule('/users/<uuid:id>/', view_func=get_user, methods=['GET'])
users_blueprint.add_url_rule('/users/<uuid:id>/', view_func=update_user_by_admin, methods=['PUT'])
users_blueprint.add_url_rule('/users/<uuid:id>/', view_func=delete_user, methods=['DELETE'])
