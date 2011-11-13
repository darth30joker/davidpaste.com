#!/usr/bin/python
#-*-coding:utf-8-*-

from flask import Module, request, session, url_for, redirect, render_template, abort
from database import db_session
from forms import *
from models import *
from functions import *

userapp = Module(__name__)
d = {}

@userapp.route('/login/', methods=['GET', 'POST'])
def login():
    pass

@userapp.route('/logout/', methods=['GET'])
def logout():
    pass

@userapp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enable=False)
    if request.method == 'POST' and form.validate_on_submit() and form.captcha.data.lower() == session['captcha'].lower():
        user = User(form.nickname.data, form.email.data, form.password.data)
        db_session.add(user)
        #try:
        db_session.commit()
        #except:
        #    abort(500)
        return redirect(url_for('login'))
    if request.method == 'GET':
        d['form'] = form
        return render_template('userapp/register.html', **d)
    abort(500)

