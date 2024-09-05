#!/usr/bin/env python3
"""
session_auth view
"""


from flask import request, jsonify
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def login():
    """
    Handles all routes for the Session authentication
    """
    email = request.form.get('email')
    if email is None or email == '':
        return (jsonify({"error": "email missing"}), 400)
    password = request.form.get('password')
    if password is None or password == '':
        return (jsonify({"error": "password missing"}), 400)

    users = User.search({'email': email})
    user = None
    if len(users) > 0:
        user = users[0]
    if user is None:
        return (jsonify({"error": "no user found for this email"}), 404)
    if user.is_valid_password(password) is False:
        return (jsonify({"error": "wrong password"}), 401)
    else:
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        cookie_name = os.getenv('SESSION_NAME')
        response.set_cookie(cookie_name, session_id)
        return response
