#!/usr/bin/env python3
"""
This module contains the Auth class
"""

from flask import request
from typing import List, TypeVar
import re


class Auth():
    """
    Manages the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require_auth
        """
        if isinstance(path, str) and path.endswith('/') is False:
            path += '/'
        value = None

        if path is None or excluded_paths is None \
           or len(excluded_paths) == 0 or path not in excluded_paths:
            value = True

        if excluded_paths is not None:
            if path in excluded_paths:
                value = False

            else:
                for p in excluded_paths:
                    if re.search(p, path) is not None:
                        value = False

        return value

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
