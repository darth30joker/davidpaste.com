#!/usr/bin/python
#-*-coding:utf-8-*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/davidpaste')
#engine = create_engine('mysql://davidpaste:davidpaste@localhost/davidpaste?charset=utf8')
#engine = create_engine('sqlite:///db.sqlite', echo=True)
db_session = scoped_session(sessionmaker(bind=engine))
