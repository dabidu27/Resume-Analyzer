from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def home(request):
    return HttpResponse('The server is up and running')

def ping(request):
    return JsonResponse({'status': 200, 'message': 'Server is running'})