#-*-coding:utf-8-*-

from models import *
from database import db_session

__all__ = ['getTags', 'getSyntaxList', 'updateTags']

def getTags():
    tags = db_session.query(Tag).all()[:10]
    return [tag.name for tag in tags]

def getSyntaxList():
    syntax = db_session.query(Syntax).order_by('name').all()
    return [(one.id, one.name) for one in syntax]

def updateTags(db_orm, paste, tags=[]):
    old_tags = [tag.name for tag in question.tags]
    tags_to_add = set(tags) - set(old_tags)
    tags_to_del = set(old_tags) - set(tags)
    if len(tags_to_add):
        for tag in tags_to_add:
            t = db_session.query(Tag).filter('LOWER(name)="%s"' % tag.strip().lower()).first()
            if not t:
                t = Tag(tag.strip())
            else:
                t.times = t.times + 1
            paste.tags.append(t)
            db_session.add(question)
    for tag in tags_to_del:
        t = db_session.query(Tag).filter('LOWER(name)="%s"' % tag.strip().lower()).first()
        if t:
            paste.tags.remove(t)
            t.times = t.times - 1
    try:
        db_session.commit()
    except Exception, e:
        db_session.rollback()
