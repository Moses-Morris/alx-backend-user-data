#!/usr/bin/env python3
"""
creating a class to manage the api auth
"""
from flask import request
from typing import TypeVar, List
import os
import uuid


class Auth():
    """class manging the api auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """handles the paths
        """
        if path:
            if isinstance(path, str):
                path = path
            else:
                path = path.path

            if not path.endswith("/"):
                path = path + "/"

        if path is None or path not in excluded_paths or \
           excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """the auth header method
        """
        if request is None:
            return None

        header = request.headers.get('Authorization')

        if header is None:
            return None
        else:
            return header

    def current_user(self, request=None) -> TypeVar('User'):
        """the current user method
        """
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request
        """
        if request is None:
            return None
        cookie_name = os.environ.get('SESSION_NAME', '_my_session_id')
        session_id = request.cookies.get(cookie_name)
        return session_id
