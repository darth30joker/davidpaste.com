#-*-coding:utf-8-*-

from flask import Module, request, session, url_for, redirect, render_template
from database import db_session
from forms import *
from models import *

tagapp = Module(__name__)
d = {}

@tagapp.route('/list/', methods=['GET'])
def list():
    pass

@tagapp.route('/create/', methods=['GET', 'POST'])
def create():
    pass

@tagapp.route('/view/', methods=['GET'])
def view():
    pass

