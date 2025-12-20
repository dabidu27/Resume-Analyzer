from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services.analysis import analyze_resume
from .models import ResumeAnalyzer

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

    if not resume or not job:
        return JsonResponse({'error': 'Missing data'}, status = 400)
    
    score, matched_keywords = analyze_resume(resume, job)

    analysis = ResumeAnalyzer.objects.create(resume_text = resume, job_text = job, match_score = score, matched_keywords = matched_keywords)
    
    return JsonResponse({'analysis_id': analysis.id, 'match_score': score, 'matched_keywords': matched_keywords})

def analyses_list(request):

    if request.method != 'GET':
        return JsonResponse({'error': 'GET Required'}, status = 405)
    
    analyses = ResumeAnalyzer.objects.all().order_by('-created_at') #the - means descending order

    data = []
    for analysis in analyses:

        data.append({'id': analysis.id, 'match_score': analysis.match_score, 'matched_keywords': analysis.matched_keywords, 'created_at': analysis.created_at.isoformat()})

    return JsonResponse(data, safe=False) #safe constrols if only dict cand be JSON serialized



