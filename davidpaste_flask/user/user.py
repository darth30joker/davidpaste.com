#!/usr/bin/python
#-*-coding:utf-8-*-
from flask import Module, render_template

user = Module(__name__)

@user.route('/register')
def register():
    return render_template('user/register.html')
