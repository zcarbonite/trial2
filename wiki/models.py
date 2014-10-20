from django.db import models
from django.utils import timezone
from time import time

def get_upload_file_name( instance, filename ):
    return '%s_%s' %( str(time()).replace('.','_'), filename )
# Create your models here.

class Article( models.Model ):
	
    title = models.CharField( max_length=300 )
    body = models.TextField()
    pub_date = models.DateTimeField( 'date published', 
                                default=timezone.now )
    likes = models.IntegerField( default=0 )
    thumbnail = models.FileField( default='', upload_to=get_upload_file_name )

    def __str__( self ):
        return self.title

    def __unicode__( self ):
        return self.title

    def get_absolute_url( self ):
        return '/wiki/get/%i/' % self.id 
	 	
	 	
class Comment( models.Model ):

    name = models.CharField( max_length=300, default='' )
    body = models.TextField()
    pub_date = models.DateTimeField( 'date published', 
                                default=timezone.now )
    likes = models.IntegerField( default=0 )
    article = models.ForeignKey( Article )

    
    def __str__( self ):
       return self.name

    def __unicode__( self ):
        return self.name
