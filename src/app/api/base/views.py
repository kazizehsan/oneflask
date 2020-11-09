from flask import current_app, jsonify, request, make_response


def unhandled_exception(error):
    current_app.logger.error(error)
    return jsonify({
        'success': False,
        'message': f'{str(error)}'
    }), 500


def page_not_found(error):
    current_app.logger.error('Page not found: %s', request.path)
    return make_response(jsonify({
        'success': False,
        'message': f'{str(error)}'
    })), 404


def internal_server_error(error):
    current_app.logger.error('Server Error: %s', error)
    return make_response(jsonify({
        'success': False,
        'message': f'{str(error)}'
    })), 500
