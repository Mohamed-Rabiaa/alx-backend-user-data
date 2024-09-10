#!/usr/bin/env python3
"""
This module contains the auth class
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
import bcrypt
from typing import Union


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

    def create_session(self, email: str) -> str:
        """
        """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Searches the user by his session id and returns the User object

        Args:
            session_id (str): The session id attribute of the User object

        Returns:
            User: The User object
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """
        Updates the corresponding user’s session ID to None
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=token)
        return token


def _hash_password(password: str) -> bytes:
    """
    Hashes a password

    Args:
        password (str): The password to hash

    Returns:
        (bytes): The hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates a new uuid and returns its
    string representaiton

    Returns:
        str: A string representation of the generated UUID
    """
    return str(uuid.uuid4())
