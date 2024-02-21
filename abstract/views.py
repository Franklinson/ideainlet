from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.


def home(request):
    return HttpResponse('Home page')

def abstract(request):
    abstracts = Abstract.objects.all()
    # topics = Topic.objects.all()
    # presentations = Presentation_type.objects.all()
    return render(request, 'abstract/abstract.html', {'abstracts': abstracts})

def author(request, pk):
    authors = Author.objects.get(id=pk)
    # abstracts = Abstract.objects.all()

    abstracts = authors.abstract_set.all()
    abstract_count = abstracts.count()

    context = {'authors': authors, 'abstracts': abstracts, 'abstract_count': abstract_count}
    return render(request, 'abstract/author.html', context)

def reviewer(request):

    authors = Author.objects.all()
    abstracts = Abstract.objects.all()
    status = Statuse.objects.all()

    total_author = authors.count()
    total_abstract = abstracts.count()
    accepted = status.filter(status='Accepted').count


    context = {'authors': authors, 'abstracts': abstracts, 
               'total_author':total_author, 'total_abstract':total_abstract,
               'accepted':accepted}
    return render(request, 'abstract/reviewer.html', context)