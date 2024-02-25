from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import AbstractForm, CreateUserForm, AuthorForm
from .filters import AuthorFilter, AbstractFilter
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import unautheticated_user, allowed_users, admin_only

# Create your views here.
@unautheticated_user
def registerPage(request):
    
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        
    context = {'form': form}
    return render(request, 'abstract/register.html', context)

@unautheticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'abstract/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def home(request):
    context = {}
    return render(request, 'abstract/home.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'reviewer'])
def abstract(request):
    abstracts = Abstract.objects.all()
    # topics = Topic.objects.all()
    # presentations = Presentation_type.objects.all()
    return render(request, 'abstract/abstract.html', {'abstracts': abstracts})

@login_required(login_url='login')
@allowed_users(allowed_roles=['author', 'reviewer'])
def author(request, pk):
    author_instance = Author.objects.get(id=pk)
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
            'date_created': abstract.date_created,
            'date_updated': abstract.date_updated
        })
    
    abstract_count = abstracts.count()
    
    context = {
        'author': author_instance,
        'abstract_info': abstract_info,
        'abstract_count': abstract_count
    }
    return render(request, 'abstract/author.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['reviewer'])
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'author', 'reviewer'])
def editor(request):
    # authors = Author.objects.all()
    abstracts = Abstract.objects.all()
    status = Statuse.objects.all()

    # total_author = authors.count()
    # total_abstract = abstracts.count()
    # accepted = status.filter(status='Accepted').count


    context = {'abstracts': abstracts}
    return render(request, 'abstract/editor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'author', 'reviewer'])
def createAbstract(request, pk):
    author = Author.objects.get(id=pk)
    form = AbstractForm(initial={'author': author})
    if request.method == 'POST':
        form =AbstractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/reviewer')

    context = {"form": form}
    return render(request, 'abstract/abstract_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'author', 'reviewer'])
def updateAbstract(request, pk):
    abstract = Abstract.objects.get(id=pk)
    form = AbstractForm(instance=abstract)

    if request.method == 'POST':
        form =AbstractForm(request.POST, instance=abstract)
        if form.is_valid():
            form.save()
            return redirect('/reviewer')
        
    context = {'form': form}
    return render(request, 'abstract/abstract_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'author', 'reviewer'])
def deleteAbstract(request, pk):
    abstract = Abstract.objects.get(id=pk)
    if request.method == "POST":
        abstract.delete()
        return redirect('/reviewer')
    context ={'item': abstract}
    return render(request, 'abstract/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'author', 'reviewer'])
def userPage(request):

    aus = request.user.author.abstract_set.all()
    # author_instance = request.user.author
    # abstracts = Abstract.objects.filter(author=author_instance)
    # abstract_info = []
    # for abstract in abstracts:
    #     topics = abstract.topics.all()  # Retrieve topics associated with the abstract
    #     topic_names = [topic.topics for topic in topics]  # Extract names of topics
    #     abstract_info.append({
    #         'id': abstract.id,
    #         'title': abstract.title,
    #         'topics': topic_names,
    #         'date_created': abstract.date_created
    #     })
    
    # abstract_count = abstracts.count()
    
    # context = {
    #     'author': author_instance,
    #     'abstract_info': abstract_info,
    #     'abstract_count': abstract_count
    # }

    context ={'aus':aus}

    return render(request, 'abstract/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['author'])
def accountSettings(request):
    author = request.user.author
    form = AuthorForm(instance=author)

    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            # Redirect to a success URL after saving the form
            return redirect('/user')  # Change 'success-url' to your desired URL

    context = {'form': form}
    return render(request, 'abstract/account_settings.html', context)