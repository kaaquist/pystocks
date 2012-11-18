from django.conf.urls import patterns, include, url


urlpatterns = patterns('pystocks.apps.collector.service',
	(r'^tweets/(?P<stock_symbol>\w+)$', 'query_company'),
	(r'^companies$', 'company_list'),
	(r'^quotes/(?P<stock_symbol>\w+)$', 'quotes'),
)