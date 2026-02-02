from django.urls import path
from . import views
from .views import register_view, login_view

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),

    path('register/', views.register_view, name='register'),
    path('features/', views.features_view, name='features'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('faqs/', views.faqs_view, name='faqs'),
    path('contact/', views.contact_view, name='contact'),
    path('reports/', views.seo_report_view, name='reports'),
   
]






