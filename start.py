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

@app.route('/about')
def about():
    return render_template('about.html')

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

@app.errorhandler(404)
def page_not_found(error):
    d['title'] = u'页面不存在'
    d['message'] = u'您所访问的页面不存在, 是不是打错地址了啊?'
    return render_template('error.html', **d), 404

@app.errorhandler(500)
def page_error(error):
    d['title'] = u'页面出错啦'
    d['message'] = u'您所访问的页面出错啦! 待会再来吧!'
    return render_template('error.html', **d), 500

if __name__ == '__main__':
	#app.run()
	app.run(debug=True)

