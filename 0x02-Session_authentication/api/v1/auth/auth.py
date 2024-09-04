#!/usr/bin/env python3
"""
This module contains the Auth class
"""

from flask import request
from typing import List, TypeVar
import re
import os


class Auth():
    """
    Manages the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for the given path.
        Returns True if the path is not in excluded_paths.
        """
        if path is None:
            return True

        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path += '/'

            pattern = re.escape(excluded_path).replace(r'\*', '.*')

            if re.fullmatch(pattern, path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization_header
        """
        if request is None:
            return None
        # value will be None if request doesn’t contain the header key
        # Authorization
        value = request.headers.get('Authorization')
        return value

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current_user
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        """
        if request is None or os.getenv('SESSION_NAME') != '_my_session_id':
            return None
        else:
            return request.cookies.get('_my_session_id')
