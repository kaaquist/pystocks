from django.conf.urls import patterns

urlpatterns = patterns('pystocks.apps.demo.views',
	(r'^diff/(?P<stock_symbol>\w+)$', 'diff'),
	(r'^diff_ajax/$', 'diff_ajax'),
)