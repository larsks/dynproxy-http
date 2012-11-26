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

Base = declarative_base()
Session = sessionmaker()

class Backend (Base):
    __tablename__ = 'backends'
    name = Column(String, primary_key=True)
    ipaddr = Column(String, nullable=True)

    def as_dict(self):
        return {
                'name': str(self.name),
                'ipaddr': str(self.ipaddr),
                }

def initmodel(dburi, echo=False):
    engine = create_engine(dburi, echo=echo)
    Base.metadata.create_all(engine)
    Session.configure(bind=engine)

