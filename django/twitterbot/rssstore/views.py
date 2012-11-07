# Create your views her
import json
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import loader
from django.template.context import Context, RequestContext
from django.views.decorators.csrf import csrf_exempt

from couchbase.couchbaseclient import VBucketAwareCouchbaseClient 

@csrf_exempt
def load(request):
   couchbase = VBucketAwareCouchbaseClient("http://localhost:8091/pools/default", "default", "")
   a,b,c = couchbase.get('allrssfeeds')
   rss_dict = json.loads(c)
   return render_to_response('template/home.html',
            {'title': 'allrssfeeds', 'feeds': _filter_invalid(rss_dict)})

@csrf_exempt
def remove(request):
   couchbase = VBucketAwareCouchbaseClient("http://localhost:8091/pools/default", "default", "")
   which_rss = request.raw_post_data
   a,b,c = couchbase.get('allrssfeeds')
   print c
   rss_dict = json.loads(c)
   for item in rss_dict:
      if item['url'] == which_rss:
         item['status'] = 'invalid'
         break
   print rss_dict
   print which_rss
   couchbase.set('allrssfeeds', 0, 0,json.dumps(rss_dict))
   a,b,c = couchbase.get('allrssfeeds')
   return render_to_response('template/home.html',
         {'title': 'allrssfeeds', 'feeds':_filter_invalid(rss_dict)}) 

def _filter_invalid(rss_dict):
   filtered = []
   for item in rss_dict:
      if item['status'] != 'invalid':
         filtered.append(item)
   return filtered

@csrf_exempt
def add(request):
   couchbase = VBucketAwareCouchbaseClient("http://localhost:8091/pools/default", "default", "")
   a,b,c = couchbase.get('allrssfeeds')
   rss_dict = json.loads(c)   
   new_feed = request.raw_post_data
   found = False
   for item in rss_dict:
      if item['url'] == new_feed:
         found = True
         break
   if not found:
      rss_dict.append({'url':new_feed, 'status':'valid'})
   couchbase.set('allrssfeeds', 0, 0,json.dumps(rss_dict))
   return render_to_response('template/home.html',
            {'title': 'allrssfeeds', 'feeds': _filter_invalid(rss_dict)})
