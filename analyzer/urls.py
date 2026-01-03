from django.urls import path
from . import views
from .views import (
    AnalysisDetailView,
    AnalysisListView,
    ResumeUploadView,
    RegistrationView,
    JobDescriptionUploadView,
    AnalyzeResumeView,
    TaskStatusView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("", views.home),
    path("ping/", views.ping),
    path("upload/resume/", ResumeUploadView.as_view()),
    path("upload/job/<int:analysis_id>/", JobDescriptionUploadView.as_view()),
    path("analyze/<int:analysis_id>/", AnalyzeResumeView.as_view()),
    path("analyses/", AnalysisListView.as_view()),
    path(
        "analyses/<int:pk>/", AnalysisDetailView.as_view()
    ),  # <int:analysis_id> tells django that there is a variable that should be used when the function of the view is called
    # when we use, cbvs, we need <int:pk>
    path("task/status/<str:task_id>/", TaskStatusView.as_view()),
    path("login/", obtain_auth_token),
    path("register/", RegistrationView.as_view()),
]
