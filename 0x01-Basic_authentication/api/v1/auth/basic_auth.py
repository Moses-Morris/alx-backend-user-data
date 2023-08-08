#!/usr/bin/env python3
""" Basic Auth Class
"""
from api.v1.auth.auth import Auth
import typing
import base64


class BasicAuth(Auth):
    """ Inherits from Auth Class
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ Return a base 64 encoding
        """
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header.startswith("Basic "):
            return "".join(authorization_header.split(" ")[1:])
