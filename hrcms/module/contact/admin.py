
from django.contrib.comments.models import Comment
from django.contrib.comments.admin import CommentsAdmin

from webcms.models import webcms_admin

webcms_admin.register(Comment, CommentsAdmin)
