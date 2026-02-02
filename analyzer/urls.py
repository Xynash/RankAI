from django.urls import path
from .views import analyze_api

urlpatterns = [
    path("analyze/", analyze_api, name="analyze_api"),
    
]
