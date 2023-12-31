#!/usr/bin/env python3
""" The Auth and password protection """
import bcrypt
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """ Salted hash """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """ generate UUID """
    return str(uuid.uuid4())


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
        ''' def valid login '''
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Create user session"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Get user from session ID """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            if not user or user is None:
                return None

            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy User Session """
        if user_id:
            self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Generate reset password token """
        try:
            user = self._db.find_user_by(email=email)
            if not user or user is None:
                raise ValueError("No user Found")

            reset_token = _generate_uuid()
            user.reset_token = reset_token
        except NoResultFound:
            raise ValueError("No user Found")
        else:
            return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ Update password for user with token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            h_password = _hash_password(password)
            self._db.update_user(user.id, hashed_password=h_password,
                                 reset_token=None)
            return None
        except Exception:
            raise ValueError
