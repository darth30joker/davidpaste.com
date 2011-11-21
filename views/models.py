#!/usr/bin/python
#-*-coding:utf-8-*-
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy import Table, MetaData, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from database import engine
from datetime import datetime
import hashlib
import random

__all__ = ['User', 'Syntax', 'Paste', 'Tag']

Base = declarative_base()
metadata = Base.metadata

paste_user = Table('pastes_users', metadata,
             Column('paste_id', Integer, ForeignKey('pastes.id')),
             Column('user_id', Integer, ForeignKey('users.id')),
        )

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

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(45), unique=True) # 登陆使用的
    nickname = Column(String(45)) # 显示时用的
    password = Column(String(45))
    paste_num = Column(Integer, default=0)
    created_time = Column(DateTime, default=datetime.now())
    modified_time = Column(DateTime, default=datetime.now())

    favourites = relationship('Paste', secondary=paste_user, backref="users")

    def __init__(self, nickname, email, password):
        self.nickname = nickname
        self.email = email
        self.password = hashlib.md5(password).hexdigest()

    def __repr__(self):
        return "<User (%s@%s)>" % (self.nickname, self.email)

class Paste(Base):
    __tablename__ = 'pastes'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    syntax_id = Column(Integer, ForeignKey('syntax.id'))
    title = Column(String(45), default=u'未知标题')
    content = Column(Text)
    views = Column(Integer, default=0)
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

    def isFavourited(self, user):
        return self in user.favourites

if __name__ == '__main__':
    from database import db_session
    metadata.create_all(engine)

    """
    syntax_dict = {'python':'Python',
                   'c':'C',
                   'html':('HTML', 'XHTML'),
                   'javascript':('JavaScript', 'JScript'),
                   'css':'CSS',
                   'actionscript':'ActionScript',
                   'applescript':'AppleScript',
                   'awk':'Awk',
                   'erlang':'Erlang',
                   'delphi':'Delphi',
                   'groovy':'Groovy',
                   'haskell':'Haskell',
                   'lua':'Lua',
                   'objective-c':'Objective-C',
                   'php':'PHP',
                   'perl':'Perl',
                   'ruby':'Ruby',
                   'scala':'Scala',
                   'sql':'SQL',
                   'diff':'Diff Files',
                   'xml':'XML',
                   'yaml':'YAML',
                   'java': 'JAVA',
                   'bash':'Bash',
                   'c#':'C#'}

    keys = syntax_dict.keys()
    keys.sort()
    for key in keys:
        value = syntax_dict[key]
        if isinstance(value, tuple):
            for name in value:
                syntax = Syntax(name, key)
                db_session.add(syntax)
        if isinstance(value, str):
            syntax = Syntax(value, key)
            db_session.add(syntax)
    db_session.commit()

    password = ''.join([random.choice('abcdefghij') for i in range(10)])
    user = User(u'未知用户', 'unknown@davidpaste.com',  hashlib.md5(password).hexdigest())
    db_session.add(user)
    db_session.commit()
    """
