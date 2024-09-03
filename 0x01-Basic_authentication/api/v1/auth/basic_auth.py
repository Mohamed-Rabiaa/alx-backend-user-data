#!/usr/bin/env python3
"""
This module contains the BasicAuth class
"""

from api.v1.auth.auth import Auth
from models.user import User
from base64 import b64decode
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth
    """

    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
        returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header is None \
           or not isinstance(authorization_header, str) \
           or authorization_header.startswith('Basic ') is False:
            return None
        else:
            base64_part = authorization_header.split()[1]
            return base64_part

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None \
           or not isinstance(base64_authorization_header, str):
            return None
        try:
            byte_str = b64decode(base64_authorization_header, validate=True)
            value = byte_str.decode('utf-8')
            return value
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None \
           or not isinstance(decoded_base64_authorization_header, str) \
           or ':' not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':')
        user_name = credentials[0]
        password = credentials[1]
        return (user_name, password)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str) \
           or user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users_list = User.search({'email': user_email})
        except KeyError:
            return None

        if len(users_list) == 0:
            return None
        user = users_list[0]
        if user.is_valid_password(user_pwd) is False:
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        base64_part = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(base64_part)
        email, password = self.extract_user_credentials(decoded)
        user = self.user_object_from_credentials(email, password)
        return user
