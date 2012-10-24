from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
	return HttpResponse('Hello Soren')

@csrf_exempt
def gitpull(request):
	import subprocess
	subprocess.call('sudo /home/django/pystocks/delay_deploy.sh', shell=True)
	return HttpResponse()