#!/usr/bin/env python3
"""
Flask app
"""

from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index() -> str:
    """
    index route
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'],
           strict_slashes=False)
def users():
    """
    users route
    """
    data = request.form
    email = data.get('email')
    password = data.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})

@app.route('/sessions', methods=['POST'],
           strict_slashes=False)
def login() -> str:
    """
    login route
    """
    email = request.form.get('email')
    password = request.form.get('password')
    value = AUTH.valid_login(email, password)
    if value is False:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response

@app.route('/sessions', methods=['DELETE'],
           strict_slashes=False)
def logout() -> str:
    """
    logout route
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
