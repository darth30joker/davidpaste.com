#-*-coding:utf-8-*-

from models import *
from database import db_session
import Image,ImageDraw,ImageFont,os,string,random,ImageFilter,cStringIO

__all__ = ['getTags', 'getSyntaxList', 'updateTags', 'getCaptcha']

def getCaptcha():
    string = 'test'
    im = Image.new('RGB', (100, 20), (255,255,255))
    draw = ImageDraw.Draw(im)
    draw.text((0,0), string, font=ImageFont.truetype('arial.ttf', 18), fill=(0,0,255))
    f = cStringIO.StringIO()
    im.save(f, 'GIF')
    f.seek(0)
    return [string, f]

def getTags():
    tags = db_session.query(Tag).all()[:10]
    return [tag.name for tag in tags]

def getSyntaxList():
    syntax = db_session.query(Syntax).order_by('name').all()
    return [(one.id, one.name) for one in syntax]

def updateTags(db_session, model, tags=[]):
    old_tags = [tag.name for tag in model.tags]
    tags_to_add = set(tags) - set(old_tags)
    tags_to_del = set(old_tags) - set(tags)
    if len(tags_to_add):
        for tag in tags_to_add:
            t = db_session.query(Tag).filter('LOWER(name)="%s"' % tag.strip().lower()).first()
            if not t:
                t = Tag(tag.strip())
            else:
                t.times = t.times + 1
            model.tags.append(t)
            db_session.add(model)
    for tag in tags_to_del:
        t = db_session.query(Tag).filter('LOWER(name)="%s"' % tag.strip().lower()).first()
        if t:
            model.tags.remove(t)
            t.times = t.times - 1
            db_session.add(model)
    try:
        db_session.commit()
    except Exception, e:
        db_session.rollback()
