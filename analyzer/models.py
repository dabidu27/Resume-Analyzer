from django.db import models

# Create your models here.

class ResumeAnalyzer(models.Model):

    resume_text = models.TextField()
    job_text = models.TextField()
    match_score = models.IntegerField()
    matched_keywords = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):

        return f"Anaysis {self.id} - match score = {self.match_score}"