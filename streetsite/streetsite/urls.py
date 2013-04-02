from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'streetsite.views.home', name='home'),
    url(r'home', 'streetsite.views.home', name='home'),
    url(r'fid/(.*)', 'streetsite.views.fid', name='fid'),
    url(r'zip/(.*)', 'streetsite.views.zip', name='zip'),
    url(r'zip', 'streetsite.views.zip_form', name='zip_form'),
    url(r'street/(.*)', 'streetsite.views.street', name='street'),
    url(r'pastfights', 'streetsite.views.pastfights', name='pastfights'),
    url(r'fight', 'streetsite.views.fight', name='fight'),
    url(r'streetword/(.+)', 'streetsite.views.streetword', name='streetword'),
    # url(r'^streetsite/', include('streetsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
