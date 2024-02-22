from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import AbstractForm
from .filters import AuthorFilter, AbstractFilter

# Create your views here.


def home(request):
    return HttpResponse('Home page')

def abstract(request):
    abstracts = Abstract.objects.all()
    # topics = Topic.objects.all()
    # presentations = Presentation_type.objects.all()
    return render(request, 'abstract/abstract.html', {'abstracts': abstracts})

def author(request, pk):
    author_instance = Author.objects.get(first_name=pk)
    abstracts = Abstract.objects.filter(author=author_instance)
    
    # Retrieve abstract information including topics
    abstract_info = []
    for abstract in abstracts:
        topics = abstract.topics.all()  # Retrieve topics associated with the abstract
        topic_names = [topic.topics for topic in topics]  # Extract names of topics
        abstract_info.append({
            'id': abstract.id,
            'title': abstract.title,
            'topics': topic_names,
            'date_created': abstract.date_created
        })
    
    abstract_count = abstracts.count()
    
    context = {
        'author': author_instance,
        'abstract_info': abstract_info,
        'abstract_count': abstract_count
    }
    return render(request, 'abstract/author.html', context)

def reviewer(request):

    authors = Author.objects.all()
    abstracts = Abstract.objects.all()
    status = Statuse.objects.all()

    total_author = authors.count()
    total_abstract = abstracts.count()
    accepted = status.filter(status='Accepted').count

    myfilter = AuthorFilter(request.GET, queryset=authors)
    authors = myfilter.qs

    absfilter = AbstractFilter(request.GET, queryset=abstracts)
    abstracts = absfilter.qs


    context = {'authors': authors, 'abstracts': abstracts, 
               'total_author':total_author, 'total_abstract':total_abstract,
               'accepted': accepted, 'myfilter': myfilter, 'absfilter': absfilter}
    return render(request, 'abstract/reviewer.html', context)


def editor(request):
    # authors = Author.objects.all()
    abstracts = Abstract.objects.all()
    status = Statuse.objects.all()

    # total_author = authors.count()
    # total_abstract = abstracts.count()
    # accepted = status.filter(status='Accepted').count


    context = {'abstracts': abstracts}
    return render(request, 'abstract/editor.html', context)


def createAbstract(request, pk):
    author = Author.objects.get(first_name=pk)
    form = AbstractForm(initial={'author': author})
    if request.method == 'POST':
        form =AbstractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/reviewer')

    context = {"form": form}
    return render(request, 'abstract/abstract_form.html', context)


def updateAbstract(request, pk):
    abstract = Abstract.objects.get(id=pk)
    form = AbstractForm(instance=abstract)

    if request.method == 'POST':
        form =AbstractForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('/create_abstract')
        
    context = {'form': form}
    return render(request, 'abstract/abstract_form.html', context)


def deleteAbstract(request, pk):
    abstract = Abstract.objects.get(id=pk)
    if request.method == "POST":
        abstract.delete()
        return redirect('/reviewer')
    context ={'item': abstract}
    return render(request, 'abstract/delete.html', context)