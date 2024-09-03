#!/usr/bin/env python3
"""
This module contains the BasicAuth class
"""

from api.v1.auth.auth import Auth
from base64 import b64decode
import binascii


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
        except (binascii.Error):
            return None
