#!/usr/bin/env python3
""" SQL ALCHEMY MODEL """
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, Integer
from sqlalchemy import create_engine


engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()
print(sqlalchemy.__version__)


class User(Base):
    """ Create a model """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
