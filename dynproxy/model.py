#!/usr/bin/python

import os
import sys

from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.interfaces import PoolListener
from sqlalchemy.sql.expression import func, select
import yaml

Base = declarative_base()
Session = sessionmaker()

class DictSerializable(object):
    def as_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            result[key] = str(getattr(self, key))
        return result

class Backend (Base, DictSerializable):
    __tablename__ = 'backends'
    name = Column(String, primary_key=True)
    ipaddr = Column(String, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)

def initmodel(dburi, echo=False):
    engine = create_engine(dburi, echo=echo)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

