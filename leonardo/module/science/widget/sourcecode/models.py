# -#- coding: utf-8 -#-

from pygments import highlight
from pygments.lexers import PythonLexer, HtmlDjangoLexer, HtmlLexer, CssLexer, JavascriptLexer, XmlLexer, JavaLexer, BashLexer
from pygments.formatters import HtmlFormatter

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from webcms.models import Widget

SYNTAX_CHOICES = (
    ('html', u'HTML'),
    ('xml', u'XML'),
    ('css', u'CSS'),
    ('js', u'JavaScript'),
    ('java', u'Java'),
    ('python', u'Python'),
    ('django', u'Django'),
    ('bash', u'Bash'),
)

class SourceCodeWidget(Widget):

    syntax = models.CharField(max_length=30, verbose_name=_("syntax"), choices=SYNTAX_CHOICES, default="html")
    code = models.TextField(verbose_name=_("code"))

    class Meta:
        abstract = True
        verbose_name = _("source code")
        verbose_name_plural = _("source codes")

    def render_content(self, options):
        if self.syntax == 'html': lexer = HtmlLexer()
        elif self.syntax == 'xml': lexer = XmlLexer()
        elif self.syntax == 'css': lexer = CssLexer()
        elif self.syntax == 'js': lexer = JavascriptLexer()
        elif self.syntax == 'java': lexer = JavaLexer()
        elif self.syntax == 'python': lexer = PythonLexer()
        elif self.syntax == 'django': lexer = HtmlDjangoLexer()
        elif self.syntax == 'bash': lexer = BashLexer()
        else: lexer = HtmlLexer()
        return render_to_string(self.template_name, { 
            'widget': self,
            'request': options['request'],
            'content': highlight(self.code, lexer, HtmlFormatter())
,
        })
