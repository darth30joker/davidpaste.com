#!/usr/bin/python
#-*-coding:utf-8-*-
from flask import Module, request, session, url_for, redirect, render_template
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from forms import *
from database import db_session
from models import *

paste = Module(__name__)
d = {}

def getTagObject(tag_name):
    try:
        tag = db_session.query(Tag).filter('LOWER(tags.name) = "%s"' % tag_name.lower()).one()
    except Exception, e:
        tag = Tag(tag_name)
        db_session.add(tag)
        try:
            db_session.commit()
        except Exception, e:
            db_session.rollback()
            return None
    else:
        tag.times = tag.times + 1
    return tag

@paste.route('/create/', methods=['GET', 'POST'])
def create():
    form = PasteForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        if form.title.data:
            title = form.title.data
        else:
            title = 'Untitled'
        if 'user' in session:
            user_id = session['user']['id']
        else:
            user_id = 1
        model = Paste(user_id, form.syntax.data, title, form.content.data)
        db_session.add(model)
        try:
            db_session.commit()
        except Exception, e:
            pass
        else:
            if form.tag.data:
                tags = form.tag.data.split(',')
                for t in tags:
                    tag = getTagObject(t)
                    if tag:
                        model.tags.append(tag)
            return redirect(url_for('view',
                paste_id=str(hex(model.id))[2:].replace('L', '')))
    d['form'] = form
    return render_template('paste/create.html', **d)

@paste.route('/view/<paste_id>/')
def view(paste_id):
    paste_id = int(paste_id, 16)
    try:
        model = db_session.query(Paste).filter(Paste.id==paste_id).one()
    except:
        model = None
    if model:
        lexer = get_lexer_by_name(model.syntax.syntax, stripall=True)
        formatter = HtmlFormatter(linenos='table', cssclass="source")
        d['code'] = highlight(model.content, lexer, formatter)
        d['model'] = model
        return render_template('paste/view.html', **d)
    else:
        return "Error"
