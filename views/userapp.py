#!/usr/bin/python
#-*-coding:utf-8-*-

from flask import Module, request, session, url_for, redirect, render_template
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
    pass

