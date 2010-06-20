#!/usr/bin/env python
# encoding: utf-8
"""
front.py

Created by davidx on 2010-06-20.
Copyright (c) 2010 IceFox's Studio. All rights reserved.
"""
from flask import Module, render_template as render
import sys
import os

front = Module(__name__)

@front.route("/")
def index():
	return render("index.html")
	

@front.route("/paste/list/")
def paste_list():
	return "lists"
	
@front.route("/paste/create/")
def paste_create():
	return "create"
	
@front.route("/paste/view/<int:id>/")
def paste_view(id):
	return "view %d" % id

"""

@front.route("/paste/edit/<id:\d+>/")
def paste_edit():
	return "edit"
	
@front.route("/paste/delete/<id:\d+>/")
def paste_delete():
	return "delete"
	
@front.route("/paste/comment/<id:\d+>/")
def paste_comment():
	return "comment"
"""