# -#- coding: utf-8 -#-

from django import forms
from django.contrib import comments
from django.contrib.comments.models import Comment
from django.db import models
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

COMMENT_TYPES = (
    ('linear', _('linear')),
    ('hierarchical', _('tree')),
)

class CommentsWidget(Widget):
    enabled = models.BooleanField(_('enabled'), default=True, help_text=_('New comments may be added'))
    count = models.BooleanField(_('count'), default=True, help_text=_('Number of comments displayed'))
    on_top = models.BooleanField(_('display on top'), default=False, help_text=_('Display input on top'))
    type = models.CharField(_('type'), max_length=155, choices=COMMENT_TYPES, default='linear', help_text=_('Type of the comments'))

    class Meta:
        abstract = True
        verbose_name = _('comments')
        verbose_name_plural = _('comments')

    @classmethod
    def initialize_type(cls):
        from feincms.admin.editor import ItemEditorForm
        class CommentsWidgetAdminForm(ItemEditorForm):
            def __init__(self, *args, **kwargs):
                super(CommentsWidgetAdminForm, self).__init__(*args, **kwargs)
                parent = kwargs.get('instance', None)
                if parent is not None:
                    f = self.fields['enabled']
                    r = f.help_text
                    r += u'<hr />'
                    for c in Comment.objects.for_model(parent.parent).order_by('-submit_date'):
                        r += '<div class="form-row" style="margin-left: 60px;"># %d <a href="/admin/comments/comment/%d/">%s</a> - %s</div>' % \
                            ( c.id, c.id, c.comment[:80], c.is_public and _('public') or _('not public') )
                    f.help_text = r

        cls.feincms_item_editor_form = CommentsWidgetAdminForm

    def render_content(self, options):

        request = options.pop('request')

        comment_page = self.parent
        parent_type = self.parent.__class__.__name__.lower()
        if hasattr(comment_page, 'original_translation') and comment_page.original_translation:
            comment_page = comment_page.original_translation

        form = None
        if self.enabled and request.POST:

            # I guess the drawback is that this page can't handle any other types of posts
            # just the comments for right now, but if we just post to the current path
            # and handle it this way .. at least it works for now.

            #extra = request._feincms_appcontent_parameters.get('page_extra_path', ())
            #if len(extra) > 0 and extra[0] == u"post-comment":

            from django.contrib.comments.views.comments import post_comment
            r = post_comment(request)
            if not isinstance(r, HttpResponseRedirect):
                form = comments.get_form()(comment_page, data=request.POST)

        if form is None:
            form = comments.get_form()(comment_page)

        context_instance = RequestContext(request, {
            'widget': self,
            'request': request,
            'form': form,
        })
        return render_to_string(self.template_name, context_instance)
