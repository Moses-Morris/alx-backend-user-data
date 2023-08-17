#!/usr/bin/env python3
""" Good pins for a Flask App """
from flask import Flask, jsonify, request, abort, redirect, session
from auth import Auth


AUTH = Auth()


app = Flask(__name__)


@app.route("/", methods=['GET'])
def payload() -> str:
    """returning a jsonified string"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """ Get user data from a form """
    try:
        data = request.form
        email = data.get('email')
        password = data.get('password')

        user = AUTH.register_user(email, password)
        response = {"email": user.email, "message": "user created"}
        return jsonify(response), 200
    except ValueError as e:
        response = {"message": "email already registered"}
        return jsonify(response), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """ Login sessions Response """
    email = request.form.get('email')
    password = request.form.get('password')
    log = AUTH.valid_login(email, password)
    if log:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE', 'GET'], strict_slashes=False)
def logout():
    """ logout and kill session """
    session_cookie = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_cookie)
    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ Implement profile function """
    cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(cookie)
    if user:
        return jsonify({"email": user.email})
    else:
        abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """the reset password token"""
    data = request.form
    email = data.get('email')

    user = AUTH.get_user(email)
    if user is None:
        abort(403)

    token = AUTH.get_reset_password_token(email)
    return jsonify({
        "email": user.email,
        "reset_token": token
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
