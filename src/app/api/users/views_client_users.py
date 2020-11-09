from flask import request, jsonify, abort
from marshmallow import ValidationError
from app.api.base.view_helpers import jsonify_no_content
from .serializers import ClientUserCreateSchema, ClientUserSchema, ClientUserUpdateByAdminSchema
from .models import ClientUser


def create_client_user():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400
        client_user = None
        try:
            client_user = ClientUserCreateSchema().load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation Failed',
                'errors': err.messages
            }), 422

        client_user.hash_password(client_user.password)
        client_user, api_token = client_user.save(send_signal=True)

        return jsonify({
            'data': {
                'client_user': ClientUserSchema().dump(client_user),
                'api_token': api_token
            }
        }), 201


def list_client_users():
    if request.method == 'GET':
        client_users_schema = ClientUserSchema(many=True)
        users_list = client_users_schema.dump(ClientUser.query.all())

        return jsonify({
            'data': users_list
        })


def get_client_user(id):
    if request.method == 'GET':
        client_user = ClientUser.query.filter_by(id=id).first()
        if client_user is None:
            abort(404, description="ClientUser not found")

        return jsonify({
            'data': ClientUserSchema().dump(client_user)
        })


def update_client_user(id):
    if request.method == 'PUT':
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400

        requested_user = ClientUser.query.filter_by(id=id).first()
        if requested_user is None:
            abort(404, description="ClientUser not found")

        data_update = None
        try:
            data_update = ClientUserUpdateByAdminSchema().load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation Failed',
                'errors': err.messages
            }), 422
        requested_user.update(data_update, send_signal=True)

        updated_user = ClientUser.query.filter_by(id=id).first()
        return jsonify({
            'data': ClientUserSchema().dump(updated_user)
        })


def delete_client_user(id):
    if request.method == 'DELETE':
        requested_user = ClientUser.query.filter_by(id=id).first()
        if requested_user is None:
            abort(404, description="ClientUser not found")

        requested_user.delete()
        return jsonify_no_content()
