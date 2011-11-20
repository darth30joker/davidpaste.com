#-*-coding:utf-8-*-

from flask import Module, request, session, url_for, redirect, render_template, abort
from database import db_session
from forms import *
from models import *
import simplejson as json

rankapp = Module(__name__)
d = {}

@rankapp.route('', methods=['GET'])
def rank():
    #users = db_session.query(User, Paste).filter_by()
    d['top_tags'] = db_session.query(Tag).order_by('times DESC').all()[:20]
    d['top_pastes'] = db_session.query(Paste).order_by('views DESC').all()[:10]
    d['new_pastes'] = db_session.query(Paste).order_by('created_time DESC').all()[:10]
    d['top_users'] = db_session.query(User).order_by('paste_num DESC').all()[:20]
    return render_template('rankapp/rank.html', **d)
