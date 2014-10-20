
from django.conf.urls import url, patterns, include
from .api import ArticleResource

article_resource = ArticleResource()

urlpatterns= patterns(
	'',
        
        url( r'^all/$', 'wiki.views.articles'),

        url( r'^get/(?P<article_id>\d+)/$', 'wiki.views.article'),
	
        url( r'^language/(?P<language>[a-z\-]+)/$', 'wiki.views.language' ),

        url( r'^create/$', 'wiki.views.create' ),
        
        url( r'^like/(?P<article_id>\d+)/$', 'wiki.views.like'),

        url( r'^comment/like/(?P<comment_id>\d+)/$', 
            'wiki.views.like_comment'),

        url( r'^comment/add/(?P<article_id>\d+)/$', 'wiki.views.add_comment' ),

        url(r'^search/$', 'wiki.views.search_titles' ),

        url(r'^api/', include( article_resource.urls ) ),
)
