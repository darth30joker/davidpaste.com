#-*-coding:utf-8-*-
from datetime import datetime
from sqlalchemy import create_engine, Table, ForeignKey
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.sqlite', echo=True)

Base = declarative_base()
metadata = Base.metadata

paste_tag = Table('paste_tag', metadata,
            Column('paste_id', Integer, ForeignKey('pastes.id')),
            Column('tag_id', Integer, ForeignKey('tags.id'))
        )

class Syntax(Base):
    __tablename__ = 'syntaxs'

    id = Column(Integer, primary_key=True)
    syntax = Column(String)
    name = Column(String)

    def __init__(syntax, name):
        self.syntax = syntax
        self.name = name

    def __repr__(self):
        return "<Syntax '%s' - %s>" % (self.syntax, self.name)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    email = Column(String)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return "<User %s AT <%s>>" % (self.nickname, self.email)

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    paste_id = Column(Integer, ForeignKey('pastes.id'))
    comment = Column(Text)
    created_time = Column(DateTime)

    user_id = Column(Integer, ForeignKey('users.id'))

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
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String, default="untitled")
    content = Column(Text)
    syntax_id = Column(Integer, ForeignKey('syntaxs.id'))
    created_time = Column(DateTime, default=datetime.now())
    modified_time = Column(DateTime, default=datetime.now())
    view_num = Column(Integer, default=0)
    comment_num = Column(Integer, default=0)

    #user = relationship()
    syntax = relation(Syntax, backref=backref('syntaxs'))
    tags = relation('Tag', secondary=paste_tag, backref='pastes')
    comments = relation(Comment, order_by=Comment.created_time,
                backref="pastes"
            )

    def __init__(self):
        pass

    def __repr__(self):
       return "<Paste ('%s')>" % self.id

    def get_url(self):
        return '/paste/%d/' % self.id

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    paste_num = Column(Integer, default=0)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Tag ('%s')>" % self.name

    def get_url(self):
        return '/tag/%s/' % self.name

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

if __name__ == "__main__":
    metadata.create_all(engine)


