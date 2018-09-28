from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'WebApp/home.html')

def interpreter(request):
    return render(request, 'WebApp/interpreter.html')

def result(request):
    return render(request, 'WebApp/result.html')


# Create your views here.
