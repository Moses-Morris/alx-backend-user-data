#!/usr/bin/env python3
""" Good pins for a Flask App """
from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/", methods=['GET'])
def payload() -> str:
    """returning a jsonified string"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
