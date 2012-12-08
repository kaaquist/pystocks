from django.conf.urls import patterns, include, url


urlpatterns = patterns('pystocks.apps.sentiment.service',
	(r'^afinn/(?P<stock_symbol>\w+)$', 'query_afinn_sentiment_on_company'),
	(r'^labmt/(?P<stock_symbol>\w+)$', 'query_labmt_sentiment_on_company'),
)