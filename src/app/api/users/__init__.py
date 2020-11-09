from flask import Blueprint
from . import models
from .views_admin_user import create_admin_user, list_admin_users, get_admin_user, update_admin_user, delete_admin_user
from .views_client_users import create_client_user, list_client_users, get_client_user, update_client_user, delete_client_user

users_blueprint = Blueprint('users', __name__)

users_blueprint.add_url_rule('/users/', view_func=create_admin_user, methods=['POST'])
users_blueprint.add_url_rule('/users/', view_func=list_admin_users, methods=['GET'])
users_blueprint.add_url_rule('/users/<int:id>/', view_func=get_admin_user, methods=['GET'])
users_blueprint.add_url_rule('/users/<int:id>/', view_func=update_admin_user, methods=['PUT'])
users_blueprint.add_url_rule('/users/<int:id>/', view_func=delete_admin_user, methods=['DELETE'])

users_blueprint.add_url_rule('/clients/', view_func=create_client_user, methods=['POST'])
users_blueprint.add_url_rule('/clients/', view_func=list_client_users, methods=['GET'])
users_blueprint.add_url_rule('/clients/<uuid:id>/', view_func=get_client_user, methods=['GET'])
users_blueprint.add_url_rule('/clients/<uuid:id>/', view_func=update_client_user, methods=['PUT'])
users_blueprint.add_url_rule('/clients/<uuid:id>/', view_func=delete_client_user, methods=['DELETE'])
