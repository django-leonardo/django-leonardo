# -#- coding: utf-8 -#-

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from webcms.models import Widget

class NowPlayingWidget(Widget):

    class Meta:
        abstract = True
        verbose_name = _("now playing")
        verbose_name_plural = _('now playing')

    def get_song(self):
        output = {}
        try:
            import MySQLdb

            db = MySQLdb.connect(host=settings.SAMDB_HOST, user=settings.SAMDB_USER, passwd=settings.SAMDB_PASSWD, db=settings.SAMDB_NAME)

            cursor = db.cursor()
            cursor.execute("SELECT * FROM historylist ORDER BY -id LIMIT 1")

            numrows = int(cursor.rowcount)

            for x in range(0,numrows):
                row = cursor.fetchone()
            output = {
                'title': row[6],
                'author': row[5],
                'album': row[7],
                'year': row[8]
            }
        except:
            pass
        return output
