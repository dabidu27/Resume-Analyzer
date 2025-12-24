from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .services.analysis import analyze_resume
from .models import ResumeAnalyzer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ResumeAnalyzerSerializer
from .pagination import AnalysisListPagination

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

# Create your views here.
def home(request):
    return HttpResponse('The server is up and running')

def ping(request):
    return JsonResponse({'status': 200, 'message': 'Server is running'})

class AnalyzeCreateView(CreateAPIView):
    
    queryset = ResumeAnalyzer.objects.all()
    serializer_class = ResumeAnalyzerSerializer

class AnalysisListView(ListAPIView):

    queryset = ResumeAnalyzer.objects.all()
    serializer_class = ResumeAnalyzerSerializer
    pagination_class = AnalysisListPagination
    
    filterset_fields = ['match_score', 'created_at'] #we set that we can filter by match_score and created_at
    ordering_fields = ['created_at', 'match_score'] #we set that we can order by created_at and match_score
    ordering = ['-created_at'] #we set default ordering by created_at, descending

class AnalysisDetailView(RetrieveAPIView):

    queryset = ResumeAnalyzer.objects.all()
    serializer_class = ResumeAnalyzerSerializer
