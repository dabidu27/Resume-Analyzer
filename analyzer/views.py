from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services.analysis import analyze_resume

# Create your views here.
def home(request):
    return HttpResponse('The server is up and running')

def ping(request):
    return JsonResponse({'status': 200, 'message': 'Server is running'})

@csrf_exempt
def analyze(request):

    if request.method != 'POST':
        return JsonResponse({'error': 'Post required'}, status = 405)
    
    data = json.loads(request.body)

    resume = data.get('resume')
    job = data.get('job')

    if not resume or not data:
        return JsonResponse({'error': 'Missing data'}, status = 400)
    
    score = 
    
    return JsonResponse({'match_score': score})

