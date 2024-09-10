#!/usr/bin/env python3
"""
This module contains the auth class
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new users

        Args:
            email (str): The email of the new user
            password (str): The password of the new user

        Returns:
            (User): The newly created User object
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))

        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return False
        hashed = user.hashed_password
        value = bcrypt.checkpw(password.encode(), hashed)
        if value is False:
            return False
        return True


def _hash_password(password: str) -> bytes:
    """
    Hashes a password

    Args:
        password (str): The password to hash

    Returns:
        (bytes): The hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
