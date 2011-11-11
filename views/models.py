#!/usr/bin/python
#-*-coding:utf-8-*-
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy import Table, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from database import engine
from datetime import datetime
import hashlib

__all__ = ['User', 'Syntax', 'Paste', 'Tag']

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(45), unique=True) # 登陆使用的
    nickname = Column(String(45)) # 显示时用的
    password = Column(String(45))
    created_time = Column(DateTime, default=datetime.now())
    modified_time = Column(DateTime, default=datetime.now())

    def __init__(self, nickname, email, password):
        self.nickname = nickname
        self.email = email
        self.password = hashlib.md5(password).hexdigest()

    def __repr__(self):
        return "<User (%s@%s)>" % (self.nickname, self.email)

class Syntax(Base):
    __tablename__ = 'syntax'

    id = Column(Integer, primary_key=True)
    name = Column(String(45)) # 显示的名字
    syntax = Column(String(45)) # pygments用的

    def __init__(self, name, syntax):
        self.name = name
        self.syntax = syntax

    def __repr__(self):
        return "<Syntax (%s)>" % self.name

paste_tag = Table('pastes_tags', metadata,
            Column('paste_id', Integer, ForeignKey('pastes.id')),
            Column('tag_id', Integer, ForeignKey('tags.id')),
        )

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String(45), unique=True)
    times = Column(Integer(11), default=1)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Tag <%s>" % self.name

class Paste(Base):
    __tablename__ = 'pastes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    syntax_id = Column(Integer, ForeignKey('syntax.id'))
    title = Column(String(45), default=u'未知标题')
    content = Column(Text)
    created_time = Column(DateTime, default=datetime.now())
    modified_time = Column(DateTime, default=datetime.now())

    user = relationship(User, backref=backref('pastes'))
    syntax = relationship(Syntax, backref=backref('pastes'))
    tags = relationship('Tag', secondary=paste_tag, order_by=Tag.name, backref="pastes")

    def __init__(self, syntax_id, title, content):
        self.user_id = None
        self.syntax_id = syntax_id
        self.title = title
        self.content = content

    def __repr__(self):
        return "<Paste (%s@%s)>" % (self.title, self.user_id)

if __name__ == '__main__':
    from database import db_session
    metadata.create_all(engine)

    syntax_dict = {'python':'Python',
                   'c':'C',
                   'html':'HTML',
                   'html':'XHTML',
                   'javascript':('JavaScript', 'JScript'),
                   'css':'CSS',
                   'c#':'C#',
                   }

    for key in syntax_dict:
        value = syntax_dict[key]
        if isinstance(value, tuple):
            for name in value:
                syntax = Syntax(name, key)
                db_session.add(syntax)
        if isinstance(value, str):
            syntax = Syntax(value, key)
            db_session.add(syntax)
    db_session.commit()
