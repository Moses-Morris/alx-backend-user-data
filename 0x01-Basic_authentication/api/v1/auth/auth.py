#!/usr/bin/env python3
""" API Authentication
"""
from flask import request
from typing import Tuple, List, TypeVar


class Auth:
    """ Class with Authentication proceedures
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Authorizes paths
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization HTTP header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Check and authorize user
        """
        return None
