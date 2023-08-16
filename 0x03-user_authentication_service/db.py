#!/usr/bin/env python3
''' Module data base '''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from user import Base, User
from typing import TypeVar
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


class DB:
    """ DB Engine """
    def __init__(self):
        ''' def init '''
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        ''' def session '''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """implementing the add user method"""
        the_user = User(email=email, hashed_password=hashed_password)
        self._session.add(the_user)
        self._session.commit()

        return the_user

    def find_user_by(self, **kwargs) -> None:
        """ Find a user in database. """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("Not Found")
        except InvalidRequestError:
            self._session.rollback()
        return user
