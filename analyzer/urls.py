from django.urls import path
from . import views
from .views import AnalysisDetailView, AnalysisListView, AnalyzeCreateView

urlpatterns = [

    path('', views.home),
    path('ping/', views.ping),
    path('analyze/', AnalyzeCreateView.as_view()),
    path('analyses/', AnalysisListView.as_view()),
    path('analyses/<int:pk>/', AnalysisDetailView.as_view()) # <int:analysis_id> tells django that there is a variable that should be used when the function of the view is called
    #when we use, cbvs, we need <int:pk>
]