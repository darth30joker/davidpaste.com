#!/usr/bin/python
#-*-coding:utf-8-*-
from flask import session
from database import db_session
from models import *
from flaskext.wtf import Form, TextField, PasswordField, TextAreaField, RecaptchaField, SelectField
from flaskext.wtf import Required, Length, Email, EqualTo, ValidationError
from functions import *

__all__ = ['RegisterForm', 'LoginForm', 'PasteForm']

class BaseForm(Form):
    pass

def email_unique(form, field):
    if len(db_session.query(User).filter_by(email=field.data).all()) > 0:
        raise ValidationError(u'这个邮件地址已经有人注册了.')

class RegisterForm(Form):
    nickname = TextField(u'昵称', [Required(), Length(min=3, max=12)])
    email = TextField(u'邮件地址', [Length(min=6, max=30),
        Email(), email_unique])
    password = PasswordField(u'密码', [Length(min=6, max=12),
        Required()])
    password_confirm = PasswordField(u'密码确认', [Required(),
        EqualTo('password', message=u'密码必须相同')])
    captcha = TextField(u'验证码', [Required()])

class LoginForm(Form):
    email = TextField(u'邮件地址', [
        Required(),
        Length(min=6, max=30),
        Email()])
    password = PasswordField(u'密码', [
        Length(min=6, max=12),
        Required()])
    captcha = TextField(u'验证码', [Required()])

class PasteForm(Form):
    title = TextField(u'标题')
    syntax = SelectField(u'语法', choices=getSyntaxList(), coerce=int)
    content = TextAreaField(u'代码', [Required(message=u"代码不能为空")])
    tag = TextField(u'标签')
    captcha = TextField(u'验证码', [Required()])

