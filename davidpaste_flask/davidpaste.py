#!/usr/bin/env python
# encoding: utf-8
"""
davidpaste.py

Created by davidx on 2010-06-20.
Copyright (c) 2010 IceFox's Studio. All rights reserved.
"""
from flask import Flask, current_app
from frontsite import front
import sys
import os

app = Flask(__name__)
app.register_module(front)

if __name__ == '__main__':
	app.run(debug=True)

