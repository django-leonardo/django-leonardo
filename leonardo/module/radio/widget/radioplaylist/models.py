# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

STATE_CHOICES = (
    ('history', _('history')),
    ('future', _('future')),
)

class RadioPlaylistWidget(Widget):
    state = models.CharField(max_length=255, verbose_name=_("playlist state"), choices=STATE_CHOICES)
    count = models.IntegerField(verbose_name=_("number of items"), default=5)

    class Meta:
        abstract = True
        verbose_name = _("radio playlist")
        verbose_name_plural = _('radio playlists')

    def get_song_list(self):
        output = []

        try:
            import MySQLdb

            db = MySQLdb.connect(host=settings.SAMDB_HOST, user=settings.SAMDB_USER, passwd=settings.SAMDB_PASSWD, db=settings.SAMDB_NAME)

            cursor = db.cursor()
            cursor.execute("SELECT * FROM historylist ORDER BY -id LIMIT 6")

            numrows = int(cursor.rowcount) - 1
            row = cursor.fetchone()

            for x in range(0,numrows):
                row = cursor.fetchone()
                output.append({
                    'title': row[5],
                    'author': row[6],
                    'album': row[7],
                    'year': row[8]
                })
        except:
            pass
        return output
