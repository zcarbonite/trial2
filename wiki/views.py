from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.utils import timezone
from django.conf import settings
import logging

#from whoosh.index import open_dir
#from whoosh.qparser import QueryParser
#from haystack.query import SearchQuerySet


from .models import Article, Comment
from .forms import ArticleForm, CommentForm


logr = logging.getLogger(__name__)

def articles( request ):

    language =  'en-gb'
    session_language = 'en-gb'

    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']


    if 'lang' in request.session:
        session_language = request.session['lang']

    args = {}
    args.update( csrf( request ) )
    args['articles'] = Article.objects.order_by('-pub_date')
    args['language'] = language
    args['session_language'] = session_language

    return render_to_response( 'articles.html',  args )

def language( request, language='en-gb' ):
    response = HttpResponse('setting language to %s' % language )
    
    response.set_cookie('lang', language )
    request.session['lang'] = language

    return response


def article( request, article_id =1):

    try:
        article = Article.objects.get(id=article_id )
        form = CommentForm()
        args = {}
        args.update( csrf( request ) )
        args['article'] = article
        args['comments'] = article.comment_set.all()
        args['form'] = form

        return render_to_response( 'article.html', args )
        
    except:
        return HttpResponseRedirect( '/wiki/all/' )
    


def create( request ):
    if request.POST:
        form = ArticleForm( request.POST, request.FILES )
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/wiki/all')
    else:
        form = ArticleForm()

    args = {}
    args.update( csrf( request ) )
    args['form'] = form

    return render_to_response('create_article.html', args )


def add_comment( request, article_id ):
    
    if request.method == 'POST':
        form = CommentForm( request.POST )
        try:
            a = Article.objects.get( id=article_id )
        except:
            return HttpResponseRedirect( '/wiki/all/' )

        
        if form.is_valid():
            c = form.save( commit=False )
            c.article = a
            c.name = "%s[%i]" % ( a.title, a.comment_set.count()+1 )
            c.save()

            


    return HttpResponseRedirect( '/wiki/get/%d/' % a.id )


def like( request, article_id ):

    if article_id:
        a = Article.objects.get( id=article_id )
        a.likes += 1
        a.save()
        return HttpResponseRedirect( '/wiki/get/%d/' % a.id )

    return HttpResponseRedirect( '/wiki/all/' )


def like_comment( request, comment_id ):
    if comment_id:
        c = Comment.objects.get( id=comment_id )
        c.likes += 1
        c.save()

        return HttpResponseRedirect( '/wiki/get/%d/' % c.article.id )

    return HttpResponseRedirect( '/wiki/all/' )

# AJAX SEARCH
def search_titles( request ):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    articles = Article.objects.filter(title__contains=search_text )
    return render_to_response( 'ajax_search.html', {'articles': articles } )


#HAYSTACK SEARCH

"""
def search_titles( request ):

    articles = SearchQuerySet().autocomplete( content_auto=request.POST.get(
                                                'search_text','' ) )

    return render_to_response( 'ajax_search.html', {'articles': articles } )
"""

# WHOOSH SEARCH
"""
def search_titles( request ):

    ix = open_dir( settings.WHOOSH_INDEX )
    articles = []

    if request.method == 'POST':
        search_text = request.POST['search_text']
        if search_text is not None and search_text != u"":
            logr.debug( ix.schema )
            parser = QueryParser( 'body', schema=ix.schema )

            try:
                qry = parser.parse( search_text )
            except:
                qry = None

            if qry is not None:
                searcher = ix.searcher()
                articles = searcher.search( qry, terms=True )
                logr.debug( articles )

    return render_to_response('ajax_search.html', {'articles': articles })
"""
