import json
import logging

from leonardo_channels import Group
from leonardo_channels.auth import (channel_session_user,
                                    channel_session_user_from_http)

LOG = logging.getLogger(__name__)


@channel_session_user_from_http
def ws_add(message):
    # Add them to the right group
    Group("widgets.content").add(message.reply_channel)


@channel_session_user
def ws_disconnect(message):
    Group("widgets.content").discard(message.reply_channel)


def update_widget(widget, content=None):
    """Push new widget content."""
    msg = {
        'id': widget.fe_identifier,
        'content': content or widget.render_content({}),
    }
    Group("widgets.content").send({'text': json.dumps(msg)})
