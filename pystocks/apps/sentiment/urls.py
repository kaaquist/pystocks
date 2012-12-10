from django.conf.urls import patterns, include, url


urlpatterns = patterns('pystocks.apps.sentiment.service',
	(r'^afinn/(?P<stock_symbol>\w+)$', 'afinn_sentiment_on_company'),
	(r'^labmt/(?P<stock_symbol>\w+)$', 'labmt_sentiment_on_company'),
)