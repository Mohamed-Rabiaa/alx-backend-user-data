#!/usr/bin/env python3
"""
This module contains the SessionExpAuth class
"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth
    """

    def __init__(self):
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Overloads create_session
        """
        session_id = super().create_session(user_id)
        if session_id is None or isinstance(session_id, str) is False:
            return None
        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Overloads user_id_for_session_id
        """
        if session_id is None or isinstance(session_id, str) is False:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        user_id = session_dictionary.get('user_id')
        if user_id is None:
            return None

        if self.session_duration <= 0:
            return user_id

        created_at = session_dictionary.get('created_at')
        if created_at is None:
            return None

        time_delta = timedelta(seconds=self.session_duration)
        expiration_time = created_at + time_delta
        if expiration_time < datetime.now():
            return None
        return session_dictionary['user_id']
