from django.http import HttpResponse
from django.shortcuts import render
import d3generator

def diff(request, stock_symbol):

	try:
		start = request.GET.get('start')
		if start:
			start = int(start)
		end = request.GET.get('end')
		if end:
			end = int(end)
	except:
		return HttpResponse('Start and end parameters must be in valid UNIX timestamp format', status=400)

	data = d3generator.generate_d3(stock_symbol, start=start, end=end)
	if data == None:
		return HttpResponse('Could not find data for %s' % (stock_symbol))
	width = request.GET.get('width', '960')
	height = request.GET.get('height', '500')
	return render(request, 'diff.html', {'data': data, 'width': width, 'height': height})

def diff_ajax(request):
	return render(request, 'diff_ajax.html')
