from functools import wraps

from flask import jsonify
from flask_jwt_extended import (
    get_jwt_claims, verify_jwt_in_request, get_jwt_identity
)

from app.api import constants
from app.api.users.models import User


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['type'] == constants.TOKEN_TYPE_REGULAR and 'is_admin' in claims and claims['is_admin']:
            return fn(*args, **kwargs)
        else:
            return jsonify({
                'success': False,
                'message': 'this is accessible by admin users only',
            }), 403

    return wrapper


def api_token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['type'] == constants.TOKEN_TYPE_API:
            user_email = get_jwt_identity()
            user_obj = User.query.filter_by(email=user_email).first()
            if user_obj:
                if not user_obj.api_token.revoked:
                    return fn(*args, **kwargs)
                else:
                    return jsonify({
                        'success': False,
                        'message': 'api token has been revoked',
                    }), 403
            else:
                return jsonify({
                    'success': False,
                    'message': 'invalid api token',
                }), 401
        else:
            return jsonify({
                'success': False,
                'message': 'this is accessible by api tokens only',
            }), 403

    return wrapper
