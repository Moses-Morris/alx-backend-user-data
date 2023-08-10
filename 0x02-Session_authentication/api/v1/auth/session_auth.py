#!/usr/bin/env python3
"""
creating a new authentication mechanism
"""
import uuid
import os


from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """creating a new auth mechanism
    """
    user_id_by_session_id = {}
    session_user = user_id_by_session_id

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for user_id
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.session_user[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a user id based on session id
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        session_value = self.session_user.get(session_id)
        return session_value

    def current_user(self, request=None):
        """an overload that returns a user instance
        based on a cookie value"""
        if request is None:
            return None

        cookie_value = self.session_cookie(request)
        if not cookie_value:
            return None

        user_id = self.user_id_for_session_id(cookie_value)
        if not user_id:
            return None

        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """kill a session
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        self.user_id_by_session_id.pop(session_id, None)
        return True
