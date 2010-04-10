#-*-coding:utf-8-*-
import hashlib
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
 
def avatar(value):
    return hashlib.md5(value.lower()).hexdigest()
 
def highlight(value, syntax):
    try:
        lexer = get_lexer_by_name(syntax, stripall=True)
    except:
        lexer = get_lexer_by_name('text', stripall=True)
    content = pygments.highlight(
            value,
            lexer,
            HtmlFormatter(linenos=True, cssclass="syntax"))
    return content
