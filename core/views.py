from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

# Create your views here.
@login_required(login_url="login")
def home(request):
    return render(request, 'index.html')
@login_required(login_url="login")
def dashboard(request):
    return render(request, 'dashboard.html')

def login_view(request):
     if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

     return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created! Please log in.")
        return redirect("login")
    return render(request, "register.html")     
def features_view(request):
    return render(request, 'features.html')
@login_required(login_url="login")
def pricing_view(request):
    return render(request, 'pricing.html')
@login_required(login_url="login")
def faqs_view(request):
    return render(request, 'FAQs.html')
@login_required(login_url="login")
def contact_view(request):
    return render(request, 'contact.html')
@login_required(login_url="login")
def seo_report_view(request):
    return render(request, 'reports.html')

