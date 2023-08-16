#!/usr/bin/env python3
""" The Auth and password protection """
import bcrypt
from user import User
from db import DB


def _hash_password(password: str) -> str:
    """ Salted hash """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> bool:
        if email and password:
            user_exist = self._db._session.query(User).filter_by(email=email).first()
            if user_exist:
                hashed = user_exist.hashed_password
                if bcrypt.checkpw(password.encode('utf-8'), hashed):
                    return True
                else:
                    return False
            else:
                return False
