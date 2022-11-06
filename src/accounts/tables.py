# pylint: disable=missing-module-docstring
from sqlalchemy import (
    Column, Integer, Date, MetaData, String, Numeric, Text, ForeignKey)
from sqlalchemy.ext.declarative import declarative_base


meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
      })

Base = declarative_base(metadata=meta)


class User(Base):
    """Table to store user info"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(Text, unique=True)
    username = Column(Text, unique=True)
    password_hash = Column(Text)


class Operation(Base):
    """Table to store operations info"""
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date)
    kind = Column(String)
    amount = Column(Numeric(10, 2))
    description = Column(String, nullable=True)
