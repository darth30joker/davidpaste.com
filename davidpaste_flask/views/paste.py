#!/usr/bin/python
#-*-coding:utf-8-*-
from flask import Module

module = Module(__name__)

@module.route('/paste/view/<paste_id>')
def view(paste_id):
    pass
