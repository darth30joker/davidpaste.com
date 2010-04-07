#!/usr/bin/env python2.6
#coding:utf-8

import web

urls = (
        '', 'adminviews.back',    
        '/$', 'adminviews.index',
        '/login/', 'adminviews.login',
        '/logout/', 'adminviews.logout',
        '/tag/list/', 'adminviews.tag_list',
        '/tag/del/(.*)/', 'adminviews.tag_del',
        '/paste/list/', 'adminviews.entry_list',
        '/paste/del/(.*)/', 'adminviews.entry_del',
        '/paste/edit/(.*)/', 'adminviews.entry_edit',
    )

app_admin = web.application(urls, globals(), autoreload = True)
app_admin.add_processor(web.loadhook(adminviews.my_loadhook))
