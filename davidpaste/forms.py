#-*-coding=utf-8-*-

import web
from web import form

__all__ = [
        'paste_form'
    ]

captcha_validator = form.Validator('Captcha Code',
        lambda x: x == web.config._session.captcha)

paste_form = form.Form(
        form.Textbox('title'),
        form.Textbox('tags'),
        form.Dropdown('syntax', form.notnull),
        form.Textarea('content', form.notnull),
        form.Textbox('captcha', captcha_validator),
    )
