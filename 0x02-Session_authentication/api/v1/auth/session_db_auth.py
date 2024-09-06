#!/usr/bin/env python3
"""
This module contains the SessionDBAuth class
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import os
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionExpAuth
    """

    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession
        and returns the Session ID
        """
        if user_id is None or isinstance(user_id, str) is False:
            return None
        session_id = super().create_session(user_id)
        if session_id is None or isinstance(session_id, str) is False:
            return None

        self.user_session = UserSession(user_id=user_id, session_id=session_id)
        self.user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the User ID by requesting UserSession
        in the database based on session_id
        """
        if session_id is None or isinstance(session_id, str) is False:
            return None
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) == 0:
            return None

        session = sessions[0]
        time_delta = timedelta(seconds=self.session_duration)
        expiration_time = session.created_at + time_delta
        if expiration_time < datetime.now():
            return None
        return session.user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID
        from the request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) == 0:
            return False
        sessions[0].remove()
        return True
