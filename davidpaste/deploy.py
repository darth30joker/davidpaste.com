#!/usr/bin/env python2.6
#coding:utf-8

import web
import views
#import admin

web.debug = False

urls = (
        #'/admin', admin.app_admin,

        '^/$', 'views.paste_create',
        '^/paste/(.*)/$', 'views.paste_view',
        '^/tag/(.*)/$', 'views.tag',
        '^/captcha/$', 'views.captcha',
        """
        '^/syntax/(.*)/$', 'views.syntax',
        '^/rank/$', 'views.rank',

        '^/register/$', 'views.register',
        '^/login/$', 'views.login',
        '^/logout/$', 'views.logout',

        '^/rss.xml$', 'views.rss',
        """
        '^(.*)', 'views.notfound',
    )

#app = web.application(urls, globals(), autoreload = True)
app = web.application(urls, globals())
session = web.session.Session(
        app, web.session.DiskStore('sessions'),
        initializer={'user_id': 1, 'captcha': 0, 'isAdmin': 0})

app.add_processor(web.loadhook(views.my_loadhook))
app.add_processor(views.my_handler)
app.notfound = views.notfound
app.internalerror = views.internalerror

def getSession():
    if '_session' not in web.config:
        web.config._session = session

if __name__ == '__main__':
    getSession()
    app.run()
