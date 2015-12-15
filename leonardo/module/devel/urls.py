
from django.conf.urls import patterns, url

from .views import ModalIframeView

urlpatterns = patterns("",
                       url(r"^modal/(?P<url>.+)/$",
                           ModalIframeView.as_view(), name="modal_iframe"),
                       url(r"^modal/(?P<url>.+)/(?P<size>.+)$",
                           ModalIframeView.as_view(), name="modal_iframe"),
                       )
