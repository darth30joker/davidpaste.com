#!/usr/bin/python
#-*-coding:utf-8-*-

from flask import Module, request, session, url_for, redirect, render_template, abort, send_file
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter, ImageFormatter
from database import db_session
from forms import *
from models import *
from functions import *
import time
import Image, ImageDraw, ImageFont, cStringIO
from StringIO import StringIO

pasteapp = Module(__name__)
d = {}

def getTagObject(tag_name):
    try:
        tag = db_session.query(Tag).filter("LOWER(tags.name) = '%s'" % tag_name.lower()).one()
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

@pasteapp.route('/create', methods=['GET', 'POST'])
def create():
    form = PasteForm(request.form, csrf_enabled=False)
    if request.method == 'POST' and form.validate_on_submit() and form.captcha.data.lower() == session['captcha'].lower():
        if 'user' in session:
            user_id = session['user']['id']
        else:
            user_id = 1
        model = Paste(form.syntax.data, form.title.data, form.content.data)
        model.user_id = user_id
        if user_id != 1:
            user = db_session.query(User).get(user_id)
            user.paste_num = int(user.paste_num) + 1
            db_session.add(user)
        if form.title.data:
            model.title = form.title.data
        else:
            model.title = u'未知标题'
        db_session.add(model)
        try:
            db_session.commit()
            updateTags(db_session, model, form.tag.data.strip().split())
        except Exception, e:
            abort(500)
        else:
            return redirect(url_for('view', paste_id=model.id))
    d['form'] = form
    d['t'] = str(int(time.time()))
    return render_template('pasteapp/create.html', **d)

@pasteapp.route('/view/<paste_id>')
def view(paste_id):
    try:
        paste_id = int(paste_id)
    except:
        abort(404)
    else:
        try:
            model = db_session.query(Paste).filter(Paste.id==paste_id).one()
        except:
            model = None
        if model:
            model.views = model.views + 1
            lexer = get_lexer_by_name(model.syntax.syntax, stripall=True)
            output = request.args.get('output', 'html')
            if output == 'html':
                formatter = HtmlFormatter(linenos='table', cssclass="source")
                d['code'] = highlight(model.content, lexer, formatter)
                d['model'] = model
                return render_template('pasteapp/view.html', **d)
            if output == 'image':
                formatter = ImageFormatter(image_format='png', font_name='DejaVu Sans MONO', line_numbers=True, unicodeoutput=True)
                f = StringIO()
                highlight(model.content, lexer, formatter, outfile=f)
                f.seek(0)
                if request.args.get('attachment', 'false').lower() == 'true':
                    return send_file(f, mimetype="image/png", as_attachment=True,
                            attachment_filename='davidpaste_%s.png' % model.id)
                return send_file(f, mimetype="image/png")
        else:
            abort(404)
