from django.urls import path
from . import views

urlpatterns = [

    path('', views.home),
    path('ping/', views.ping),
    path('analyze/', views.analyze),
    path('analyses/', views.analyses_list)
]