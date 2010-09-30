#!/usr/bin/python
#-*-coding:utf-8-*-
from flask import Module, render_template

paste = Module(__name__)

@paste.route('/create')
def create():
    return render_template('paste/create.html')
