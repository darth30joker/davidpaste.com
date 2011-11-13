#-*-coding:utf-8-*-

from flask import Module, request, session, url_for, redirect, render_template, abort
from database import db_session
from forms import *
from models import *
import simplejson as json

tagapp = Module(__name__)
d = {}

@tagapp.route('/list', methods=['GET'])
def list():
    pass

@tagapp.route('/<tag_name>', methods=['GET', 'POST'])
def view(tag_name):
    tag = db_session.query(Tag).filter_by(name=tag_name).one()
    if request.method == 'GET':
        if not tag:
            abort(404)
        d['tag'] = tag
        d['pastes'] = tag.pastes[:20]
        return render_template('tagapp/view.html', **d)
    if request.method == 'POST':
        if not tag:
            return json.dump([])
        start = request.GET.get('start', 0)
        tags = tag.pastes[start-1:20]
        return json.decode(tags)

