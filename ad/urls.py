from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


from ad.views import *

urlpatterns = patterns('',
    
    (r'^$', index),
    (r'^links/$', links),
    (r'^links/(?P<page>\d+)/$', links),
    (r'^(buy|sell)/(\d+)/$', main),
    (r'^tag/(?P<tag>[^/]+)/$','ad.views.with_tag'), 
    (r'^tag/(?P<tag>[^/]+)/(?P<page>\d+)/$', 'ad.views.with_tag' ),
    (r'^init_tags$','ad.views.init_tags'),
    
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)
