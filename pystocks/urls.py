from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^v1/sentiment/', include('pystocks.apps.sentiment.urls')),
    url(r'^v1/', include('pystocks.apps.collector.urls')),
    url(r'^demo/', include('pystocks.apps.demo.urls')),
)
