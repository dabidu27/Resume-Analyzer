from django.urls import path
from . import views

urlpatterns = [

    path('', views.home),
    path('ping/', views.ping),
    path('analyze/', views.analyze),
    path('analyses/', views.analyses_list),
    path('analyses/<int:analysis_id>/', views.analyses_list_by_id) # <int:analysis_id> tells django that there is a variable that should be used when the function of the view is called
]