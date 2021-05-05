from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import ValidationError

from app.api import constants
from app.api.auth.serializers import LoginSchema
from app.api.users.models import User


def login():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return jsonify({
                'success': False,
                'message': 'No input data provided',
                'errors': {}
            }), 400

        login_schema = LoginSchema()
        try:
            user_data = login_schema.load(json_data)
        except ValidationError as err:
            return jsonify({
                'success': False,
                'message': 'Validation Failed',
                'errors': err.messages
            }), 400

        user_obj = User.query.filter_by(email=user_data['email']).first()

        if user_obj and user_obj.is_admin:
            if user_obj.is_active:
                if user_obj.check_password(user_data['password']):
                    jwt_user_claims = {
                        'type': constants.TOKEN_TYPE_REGULAR,
                        'is_admin': user_obj.is_admin
                    }
                    response_obj = {
                        'access_token': create_access_token(identity=user_obj.email, user_claims=jwt_user_claims),
                        'refresh_token': create_refresh_token(identity=user_obj.email, user_claims=jwt_user_claims),
                    }
                    return jsonify(response_obj), 200
                else:
                    return_message = 'invalid credentials'
                    status_code = 401
            else:
                return_message = 'user is inactive'
                status_code = 401
        else:
            return_message = 'invalid credentials'
            status_code = 401

        response_obj = {
            'success': False,
            'message': return_message
        }
        return jsonify(response_obj), status_code