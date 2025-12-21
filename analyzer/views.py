from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services.analysis import analyze_resume
from .models import ResumeAnalyzer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ResumeAnalyzerSerializer

# Create your views here.
def home(request):
    return HttpResponse('The server is up and running')

def ping(request):
    return JsonResponse({'status': 200, 'message': 'Server is running'})

@api_view(['POST'])
def analyze(request):
    
    serializer = ResumeAnalyzerSerializer(data = request.data)
    
    if serializer.is_valid():

        serializer.save()
        return Response(serializer.data, status = 200)

    return Response(serializer.errors, status = 400)

@api_view(['GET'])
def analyses_list(request):
    
    analyses = ResumeAnalyzer.objects.all().order_by('-created_at') #the - means descending order
    serializer = ResumeAnalyzerSerializer(analyses, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def analyses_list_by_id(request, analysis_id):

    try:
        analysis = ResumeAnalyzer.objects.get(id = analysis_id)
    except ResumeAnalyzer.DoesNotExist:
        return JsonResponse({'error': 'Analysis not found'}, status = 404)

    serializer = ResumeAnalyzerSerializer(analysis)

    return Response(serializer.data)

'''
#def analyses_list_by_id(request, analysis_id):

    if request.method != 'GET':
        return JsonResponse({'error': 'GET required'}, status = 405)
    
    try:
        analysis = ResumeAnalyzer.objects.get(id = analysis_id)
    except ResumeAnalyzer.DoesNotExist:
        return JsonResponse({'error': 'Object not found'}, status = 404)

    data = {'id': analysis.id, 'match_score': analysis.match_score, 'matched_keywords': analysis.matched_keywords, 'created_at': analysis.created_at.isoformat()}

    return JsonResponse(data)
'''
