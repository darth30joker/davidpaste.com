#!/usr/bin/env python
# encoding: utf-8
"""
davidpaste.py

Created by davidx on 2010-06-20.
Copyright (c) 2010 IceFox's Studio. All rights reserved.
"""
from flask import Flask, render_template
from paste import paste
from user import user
import sys
import os

app = Flask(__name__)
app.register_module(paste, url_prefix="/paste")
app.register_module(user)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)

