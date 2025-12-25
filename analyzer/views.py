from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import ResumeAnalyzer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ResumeAnalyzerSerializer, RegistrationSerializer, ResumeUploadSerializer, JobDescriptionUploadSerializer, AnalyzeResumeSerializer
from .pagination import AnalysisListPagination
from rest_framework.permissions import AllowAny
from .services.parse_pdf import PdfParser
from .services.analysis import ResumeAnalyzerTool
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
def home(request):
    return HttpResponse('The server is up and running')

def ping(request):
    return JsonResponse({'status': 200, 'message': 'Server is running'})

#WHEN WE USE CLASS BASED VIEWS (but not generic, just APIView), the method inside just be called post or get,
#so django knows what type of request to except, instead of using the api_view decorator
class ResumeUploadView(APIView):
    
   parser_classes = [MultiPartParser, FormParser]

   def post(self, request):
       
       serializer = ResumeUploadSerializer(data = request.data, context = {'request': request})

       serializer.is_valid(raise_exception=True)
       analysis = serializer.save()

       return Response({'analysis_id': analysis.id, 'message': 'Resume uploaded successfully'}, status=200)

class JobDescriptionUploadView(APIView):

    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, analysis_id):
        
        try:
            analysis = ResumeAnalyzer.objects.get(id = analysis_id, user = request.user)
        except ResumeAnalyzer.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
        
        #because we call the serialzier with the analysis instance, Django calls the .upload() method instead of .create() when we save, replacing the state of the same object
        serializer = JobDescriptionUploadSerializer(analysis, data = request.data, context = {'request': request})

        serializer.is_valid(raise_exception = True)
        analysis = serializer.save()

        return Response({'analysis_id': analysis_id, 'message': 'Job description successfully uploaded'}, status = 200)

class AnalyzeResumeView(APIView):

    def get(self, request, analysis_id):

        try:
            analysis = ResumeAnalyzer.objects.get(id = analysis_id, user = request.user)
        except ResumeAnalyzer.DoesNotExist:
            return Response({'error': 'Not found'}, status = 404)
        
        if not analysis.resume_text or  not analysis.job_text:
            return Response({'error': 'Missing data'}, status = 400)

        resumeAnalyzer = ResumeAnalyzerTool(analysis.resume_text, analysis.job_text)
        match_score, matched_keywords = resumeAnalyzer.analyze_resume()
        analysis.match_score = match_score
        analysis.matched_keywords = matched_keywords
        analysis.save()
        serializer = AnalyzeResumeSerializer(analysis)

        return Response(serializer.data, status = 200)


class AnalysisListView(ListAPIView):

    serializer_class = ResumeAnalyzerSerializer
    pagination_class = AnalysisListPagination
    
    filterset_fields = ['match_score', 'created_at'] #we set that we can filter by match_score and created_at
    ordering_fields = ['created_at', 'match_score'] #we set that we can order by created_at and match_score
    ordering = ['-created_at'] #we set default ordering by created_at, descending

    def get_queryset(self): #we override get_queryset so a user only gets analyses from the table that belong to him
        return ResumeAnalyzer.objects.filter(user = self.request.user)

class AnalysisDetailView(RetrieveAPIView):

    serializer_class = ResumeAnalyzerSerializer

    def get_queryset(self):
        return ResumeAnalyzer.objects.filter(user = self.request.user)


class RegistrationView(CreateAPIView):

    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny] #we override the isAuthenticated global permission because registration has to be public
