from flask import request, jsonify, abort
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, get_jti, jwt_required, get_jwt_identity
from app.api.base.view_helpers import jsonify_no_content
from .serializers import UserResponseSchema, UserCreateBySelfSchema, UserCreateByAdminSchema, UserUpdateByAdminSchema, \
    UserUpdateBySelfSchema
from .models import User, APIToken
from app.api import constants
from ..decorators import admin_required


def _create_api_token(user):
    jwt_user_claims = {
        'type': constants.TOKEN_TYPE_API,
        'is_admin': user.is_admin
    }
    access_token = create_access_token(user.email, expires_delta=False, user_claims=jwt_user_claims)
    api_token = APIToken()
    api_token.revoked = False
    api_token.user = user
    api_token.jti = get_jti(access_token)
    api_token.save()
    return access_token


def create_user_by_self():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400
        user = None
        try:
            user = UserCreateBySelfSchema().load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation Failed',
                'errors': err.messages
            }), 400
        user.is_active = True
        user.is_admin = False
        user.hash_password(user.password)
        user = user.save(send_signal=True)

        access_token = _create_api_token(user)

        return jsonify({
            'data': UserResponseSchema().dump(user),
            'api_token': access_token
        }), 201


@admin_required
def create_user_by_admin():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400
        user = None
        try:
            user = UserCreateByAdminSchema().load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation Failed',
                'errors': err.messages
            }), 400
        user.hash_password(user.password)
        user = user.save(send_signal=True)

        if not user.is_admin:
            access_token = _create_api_token(user)
            print('Sending access_token to: ' + user.email)
            print(access_token)

        return jsonify({
            'data': UserResponseSchema().dump(user)
        }), 201


@admin_required
def list_users():
    if request.method == 'GET':
        users_schema = UserResponseSchema(many=True)
        users_list = users_schema.dump(User.query.all())

        return jsonify({
            'data': users_list
        })


@jwt_required
def get_me():
    if request.method == 'GET':
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()
        if user is None:
            abort(404, description="User not found")

        return jsonify({
            'data': UserResponseSchema().dump(user)
        })


@admin_required
def get_user(id):
    if request.method == 'GET':
        user = User.query.filter_by(id=id).first()
        if user is None:
            abort(404, description="User not found")

        return jsonify({
            'data': UserResponseSchema().dump(user)
        })


@jwt_required
def update_me():
    if request.method == 'PUT':
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400

        requested_user = User.query.filter_by(email=get_jwt_identity()).first()
        if requested_user is None:
            abort(404, description="User not found")

        data_update = None
        try:
            data_update = UserUpdateBySelfSchema().load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation Failed',
                'errors': err.messages
            }), 400
        requested_user.update(data_update, send_signal=True)

        updated_user = User.query.filter_by(email=get_jwt_identity()).first()
        return jsonify({
            'data': UserResponseSchema().dump(updated_user)
        })


@admin_required
def update_user_by_admin(id):
    if request.method == 'PUT':
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400

        requested_user = User.query.filter_by(id=id).first()
        if requested_user is None:
            abort(404, description="User not found")

        if requested_user.email == get_jwt_identity():
            return jsonify({
                'success': False,
                'message': 'cannot update oneself',
            }), 403

        data_update = None
        try:
            data_update = UserUpdateByAdminSchema().load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation Failed',
                'errors': err.messages
            }), 400
        requested_user.update(data_update, send_signal=True)

        updated_user = User.query.filter_by(id=id).first()
        return jsonify({
            'data': UserResponseSchema().dump(updated_user)
        })


@admin_required
def delete_user(id):
    if request.method == 'DELETE':
        requested_user = User.query.filter_by(id=id).first()
        if requested_user is None:
            abort(404, description="User not found")

        if requested_user.email == get_jwt_identity():
            return jsonify({
                'success': False,
                'message': 'cannot delete oneself',
            }), 403

        requested_user.delete()
        return jsonify_no_content()


@admin_required
def alter_api_token_revoke_status(id):
    if request.method == 'PUT':
        requested_user = User.query.filter_by(id=id).first()
        if requested_user is None:
            abort(404, description="User not found")
        requested_user.api_token.revoked = not requested_user.api_token.revoked

        requested_user.update({}, send_signal=True)

        updated_user = User.query.filter_by(id=id).first()
        return jsonify({
            'data': UserResponseSchema().dump(updated_user)
        })


@admin_required
def create_api_token(id):
    if request.method == 'POST':
        requested_user = User.query.filter_by(id=id).first()
        if requested_user is None:
            abort(404, description="User not found")

        old_api_token = requested_user.api_token
        access_token = _create_api_token(requested_user)
        print('Sending access_token to: ' + requested_user.email)
        print(access_token)

        if old_api_token:
            old_api_token.delete()

        updated_user = User.query.filter_by(id=id).first()
        return jsonify({
            'data': UserResponseSchema().dump(updated_user)
        })
