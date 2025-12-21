from rest_framework import serializers
from .models import ResumeAnalyzer

class ResumeAnalyzerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResumeAnalyzer
        fields = ['id', 'resume_text', 'job_text', 'match_score', 'matched_keywords', 'created_at']