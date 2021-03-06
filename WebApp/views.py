from django.shortcuts import render
from django.http import HttpResponse
from . import api

def index(request):
	return render(request, 'WebApp/home.html')

def interpreter(request):
	message = request.GET.get('msg')
	
	# Tokenizer
	tokens = api.cfpl_tokenize(message)

	# Parser
	output = api.cfpl_parse(tokens)

	return HttpResponse(output)

def result(request):
	return render(request, 'WebApp/result.html')

# Create your views here.