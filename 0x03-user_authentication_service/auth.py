#!/usr/bin/env python3
""" The Auth and password protection """
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound


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

    def register_user(self, email: str, password: str) -> User:
        ''' def register user '''
        if email and password:
            try:
                self._db.find_user_by(email=email)
            except NoResultFound:
                user = self._db.add_user(email, _hash_password(password))
                return user
            else:
                raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """ validate login credentials """
        user = self._db._session.query(User).filter_by(email=email).first()
        if user:
            hashed = user.hashed_password
            state = bcrypt.checkpw(password.encode('utf-8'), hashed)
            if state:
                return True
            else:
                return False
        else:
            return False
