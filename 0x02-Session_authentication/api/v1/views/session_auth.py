#!/usr/bin/env python3
"""
flask view that handles all routes for the session auth
"""
from flask import jsonify, request, make_response, abort
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """login route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    user_json = user[0].to_json()

    response = make_response(jsonify(user_json))
    cookie_name = os.environ.get('SESSION_NAME', '_my_session_id')
    response.set_cookie(cookie_name, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_logout():
    """session i'm out
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
