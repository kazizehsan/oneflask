from flask import request, jsonify, abort
from marshmallow import ValidationError
from app.api.base.view_helpers import jsonify_no_content
from .serializers import AdminUserCreateSchema, AdminUserSchema, AdminUserUpdateByAdminSchema
from .models import AdminUser


def create_admin_user():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400
        admin_user = None
        try:
            admin_user = AdminUserCreateSchema().load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation Failed',
                'errors': err.messages
            }), 422

        admin_user.hash_password(admin_user.password)
        admin_user.save(send_signal=True)

        return jsonify({
            'data': AdminUserSchema().dump(admin_user)
        }), 201


def list_admin_users():
    if request.method == 'GET':
        admin_users_schema = AdminUserSchema(many=True)
        users_list = admin_users_schema.dump(AdminUser.query.all())

        return jsonify({
            'data': users_list
        })


def get_admin_user(id):
    if request.method == 'GET':
        admin_user = AdminUser.query.filter_by(id=id).first()
        if admin_user is None:
            abort(404, description="AdminUser not found")

        return jsonify({
            'data': AdminUserSchema().dump(admin_user)
        })


def update_admin_user(id):
    if request.method == 'PUT':
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No input data provided'
            }), 400

        requested_user = AdminUser.query.filter_by(id=id).first()
        if requested_user is None:
            abort(404, description="AdminUser not found")

        data_update = None
        try:
            data_update = AdminUserUpdateByAdminSchema().load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation Failed',
                'errors': err.messages
            }), 422
        requested_user.update(data_update, send_signal=True)

        updated_user = AdminUser.query.filter_by(id=id).first()
        return jsonify({
            'data': AdminUserSchema().dump(updated_user)
        })


def delete_admin_user(id):
    if request.method == 'DELETE':
        requested_user = AdminUser.query.filter_by(id=id).first()
        if requested_user is None:
            abort(404, description="AdminUser not found")

        requested_user.delete()
        return jsonify_no_content()
