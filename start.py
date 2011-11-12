#!/usr/bin/env python
# encoding: utf-8
"""
davidpaste.py

Created by davidx on 2010-06-20.
Copyright (c) 2010 IceFox's Studio. All rights reserved.
"""
from flask import Flask, request, render_template, session, Response, send_file
from views.pasteapp import pasteapp
from views.userapp import userapp
from views.tagapp import tagapp
from views.database import db_session
from views.forms import PasteForm
#from utils import getCaptcha
from views.filters import *
from views.functions import *

RECAPTCHA_PUBLIC_KEY = '6LeaILoSAAAAAOB1s0b5uGqDZ6Xbn1IkAR4wQpqJ'
RECAPTCHA_PRIVATE_KEY = '6LeaILoSAAAAAAKm48RO9VK5_Knup3Z3glfJ9Of8'

app = Flask(__name__)
app.config.from_object(__name__)
app.register_module(pasteapp, url_prefix="/paste")
app.register_module(userapp, url_prefix="/user")
app.register_module(tagapp, url_prefix="/tag")
app.secret_key = 'sdaghasdhsdh2346234uyqahg'
app.jinja_env.filters['dateformat'] = dateformat
app.jinja_env.filters['avatar'] = avatar

d = {}

@app.route('/')
def index():
    form = PasteForm(request.form, csrf_enabled=False)
    d['form'] = form
    d['syntax_list'] = getSyntaxList()
    return render_template('pasteapp/create.html', **d)

@app.route('/captcha')
def captcha():
    captcha = getCaptcha()
    session['captcha'] = captcha[0]
    return send_file(captcha[1], mimetype='image/gif')

@app.before_request
def before_request():
    d['session'] = session
    d['tags'] = getTags()

@app.after_request
def after_request(response):
    try:
        db_session.commit()
    except Exception, e:
        db_session.rollback()
    return response

if __name__ == '__main__':
	app.run(debug=True)

