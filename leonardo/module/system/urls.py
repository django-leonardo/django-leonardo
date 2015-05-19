from django.conf.urls import include, patterns, url


urlpatterns = patterns('',
                       url(r'^packages/', include('leonardo.module.system.package.urls')),
                       url(r'^maintenance/', include('leonardo.module.system.maintenance.urls')),
                       )
