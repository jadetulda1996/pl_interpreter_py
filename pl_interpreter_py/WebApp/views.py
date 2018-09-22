from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'WebApp/home.html')

def blahbalg(request):
    return render(request, 'WebApp/about.html')

def sample(request):
    return render(request, 'WebApp/sample.html')


# Create your views here.
