from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return HttpResponse('Home page')

def abstract(request):
    return render(request, 'abstract/abstract.html')

def author(request):
    return render(request, 'abstract/author.html')

def reviewer(request):
    return render(request, 'abstract/reviewer.html')