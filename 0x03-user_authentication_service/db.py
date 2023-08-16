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

    def find_user_by(self, **kargs) -> User:
        ''' def find user '''
        try:
            user = self._session.query(User).filter_by(**kargs).first()
        except TypeError:
            raise InvalidRequestError
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """updating a users credentials"""
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid argument: {key}")
            self._session.commit()
            return None
        except NoResultFound:
            raise NoResultFound("user not found")
        except InvalidRequestError:
            self._session.rollback()
