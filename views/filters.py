#!/usr/bin/env python
#-*-coding:utf-8-*-
import hashlib
import re

def dateformat(value, format="%Y-%m-%d %H:%M"):
    return value.strftime(format)

def avatar(value):
    return hashlib.md5(value).hexdigest()

def textformat(text):
    """docstring for format"""
    result = []
    ul_ol = '';
    bold = re.compile('\*(.+)\*')
    italy = re.compile('_(.+)_')
    url = re.compile('{(.+)\|(http://.+)}')
    img = re.compile('\[(.+)\|(http://.+)\]')
    for line in text.split('\n'):
        line = line.lstrip()
        if ul_ol:
            if (ul_ol == 'ol' and not line.startswith('= ')) or \
                    (ul_ol == 'ul' and not line.startswith('- ')):
                result.append('</%s>' % ul_ol)
                ul_ol = ''
        bolds = bold.findall(line)
        if bolds:
            for one in bolds:
                line = line.replace('*%s*' % one, '<strong>%s</strong>' % one)
        italies = italy.findall(line)
        if italies:
            for one in italies:
                line = line.replace('_%s_' % one, '<em>%s</em>' % one)
        urls = url.findall(line)
        if urls:
            for one in urls:
                line = line.replace('{%s|%s}' % (one[0], one[1]),
                            '<a href="%s">%s</a>' % (one[1], one[0]))
        imgs = img.findall(line)
        if imgs:
            for one in imgs:
                line = line.replace('[%s|%s]' % (one[0], one[1]),
                            '<img alt="%s" src="%s" />' % (one[0], one[1]))
        if line == '':
            result.append('<br />')
        elif line.startswith('##### '):
            result.append('<h5>%s</h5>' % line.replace('#', '').strip())
        elif line.startswith('#### '):
            result.append('<h4>%s</h4>' % line.replace('#', '').strip())
        elif line.startswith('### '):
            result.append('<h3>%s</h3>' % line.replace('#', '').strip())
        elif line.startswith('## '):
            result.append('<h2>%s</h2>' % line.replace('#', '').strip())
        elif line.startswith('# '):
            result.append('<h1>%s</h1>' % line.replace('#', '').strip())
        elif line.startswith('= '):
            if not ul_ol:
                result.append('<ol>')
                ul_ol = 'ol'
            result.append('<li>%s</li>' % line.replace('= ', '').strip())
        elif line.startswith('- '):
            if not ul_ol:
                result.append('<ul>')
                ul_ol = 'ul'
            result.append('<li>%s</li>' % line.replace('- ', '').strip())
        else:
            result.append(line + '<br />')
    return ''.join(result)

if __name__ == '__main__':
    text = """Hello, everyone
    let's have a test for this format of text.
    # Title one
    ## Title two
    ### Title three
    #### Title four
    ##### Title five

    *bold me*

    _italy me_

    {davidx's blog|http://davidx.me/}
    [show me|http://davidx.me/1.jpg]

    = one
    = two
    = three
    - first
    - second
    - third

    Is it ok?
    """
    
    print format(text)