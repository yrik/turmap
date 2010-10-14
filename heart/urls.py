from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()


from heart.views import *

urlpatterns = patterns('',
    
    (r'^$', index),
    (r'^tag/(?P<tag>[^/]+)/$','ad.views.with_tag'),
    (r'^tag/(?P<tag>[^/]+)/(?P<page>\d+)/$', 'ad.views.with_tag' ),
    (r'^init_tags$','ad.views.init_tags'),
    
    #admin
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('',
    (r'', include('gmapi.urls.media')), # Use for debugging only.
        (r'^$', 'myapp.views.index'),
    )

