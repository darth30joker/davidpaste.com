#!/usr/bin/env python
# encoding: utf-8
"""
davidpaste.py

Created by davidx on 2010-06-20.
Copyright (c) 2010 IceFox's Studio. All rights reserved.
"""
from flask import Flask, request, render_template, session, Response, send_file
from paste import paste
from database import db_session
from forms import PasteForm
from utils import getCaptcha

RECAPTCHA_PUBLIC_KEY = '6LfJ4L4SAAAAAP9nayBSvOiUcokpz8w5YV0f5oBZ'
RECAPTCHA_PRIVATE_KEY = '6LfJ4L4SAAAAANelSs7KKb3y-VOPsEyUaM3-8Pwx'

app = Flask(__name__)
app.config.from_object(__name__)
app.register_module(paste, url_prefix="/paste")
app.secret_key = 'sdaghasdhsdh2346234uyqahg'

d = {}

@app.route('/')
def index():
    form = PasteForm(request.form)
    d['form'] = form
    return render_template('paste/create.html', **d)

@app.route('/captcha/')
def captcha():
    captcha = getCaptcha()
    session['captcha'] = captcha[0]
    return send_file(captcha[1], mimetype='image/gif')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    pass

@app.route('/logout/', methods=['GET'])
def logout():
    pass

"""
@app.before_request
def before_request():
    d['session'] = session
"""

@app.after_request
def after_request(response):
    try:
        db_session.commit()
    except Exception, e:
        db_session.rollback()
    return response

if __name__ == '__main__':
	app.run(debug=True)

