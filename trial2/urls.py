from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    (r'^admin/', include(admin.site.urls)),

    (r'^wiki/', include( 'wiki.urls' ) ),
    ( r'^accounts/', include( 'userprofile.urls' ) ),

    url(r'^accounts/login/$', 'trial2.views.login' ),
    url(r'^accounts/auth/$', 'trial2.views.auth_view' ),
    url(r'^accounts/logout/$', 'trial2.views.logout' ),
    url(r'^accounts/loggedin/$', 'trial2.views.loggedin' ),
    url(r'^accounts/invalid/$', 'trial2.views.invalid_login' ),

    url(r'^accounts/register/$', 'trial2.views.register_user'),
    url(r'^accounts/register_success/$', 'trial2.views.register_success'),

    url(r'^$', 'trial2.views.home', name='home' ),

#    url(r'^search/', include('haystack.urls' ) ),


)
