#!/usr/bin/env python
# encoding: utf-8
"""
davidpaste.py

Created by davidx on 2010-06-20.
Copyright (c) 2010 IceFox's Studio. All rights reserved.
"""
from flask import Flask, render_template
from flaskext.sqlalchemy import SQLAlchemy
from paste import paste
from user import user
from models import *
import sys
import os

app = Flask(__name__)
app.config.from_pyfile('db.cfg')
app.register_module(paste, url_prefix="/paste")
app.register_module(user)
db = SQLAlchemy(app)


@app.route('/')
def index():
    models = db.session.query(Syntax).all()
    return render_template('index.html')

"""
@app.before_request
def before_request():
"""

if __name__ == '__main__':
	app.run(debug=True)

