from django.conf.urls import patterns, url
from django.conf.urls.defaults import *

urlpatterns = patterns('',url(r'^$', 'twitterbot.rssstore.views.load'),
                        (r'^add', 'twitterbot.rssstore.views.add'),
                        (r'^remove', 'twitterbot.rssstore.views.remove'))
