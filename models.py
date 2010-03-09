#-*-coding:utf-8-*-
from datetime import datetime
from sqlalchemy import create_engine, Table, ForeignKey
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:root@localhost/davidblog?charset=utf8', echo=False)

Base = declarative_base()
metadata = Base.metadata

paste_tag = Table('paste_tag', metadata,
            Column('paste_id', Integer, ForeignKey('entries.id')),
            Column('tag_id', Integer, ForeignKey('tags.id'))
        )

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    paste_id = Column(Integer, ForeignKey('entries.id'))
    email = Column(String)
    username = Column(String)
    url = Column(String)
    comment = Column(Text)
    created_time = Column(DateTime)

    def __init__(self, paste_id, username, email, url, comment):
        self.paste_id = paste_id
        self.username = username
        self.email = email
        self.url = url
        self.comment = comment
        self.created_time = datetime.now()

class Paste(Base):
    __tablename__ = 'pastes'

    id = Column(Integer, primary_key=True)
    title = Column(String, default="untitled")
    syntax = Column(Integer)
    content = Column(Text)
    created_time = Column(DateTime, default=datetime.now())
    modified_time = Column(DateTime, default=datetime.now())
    view_num = Column(Integer, default=0)
    comment_num = Column(Integer, default=0)

    tags = relation('Tag', secondary=entry_tag, backref='entries')
    comments = relation(Comment, order_by=Comment.created_time,
                backref="entries"
            )

    def __init__(self, title, syntax, content):
        self.title = title
        self.syntax = syntax
        self.content = content

    def __repr__(self):
       return "<Paste ('%s')>" % self.id

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    paste_num = Column(Integer, default=0)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tag ('%s')>" % self.name

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
