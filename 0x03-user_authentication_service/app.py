#!/usr/bin/env python3
""" Good pins for a Flask App """
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
