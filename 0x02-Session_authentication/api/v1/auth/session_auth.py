#!/usr/bin/env python3
"""
This module contains the SessionAuth class
"""

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    SessionAuth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id
        """
        if user_id is None or isinstance(user_id, str) is False:
            return None
        else:
            session_id = str(uuid.uuid4())
            type(self).user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID
        """
        if session_id is None or isinstance(session_id, str) is False:
            return None
        user_id = type(self).user_id_by_session_id.get(session_id)
        return user_id
