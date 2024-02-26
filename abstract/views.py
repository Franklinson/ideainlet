from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import AbstractForm, CreateUserForm, AuthorForm, ContactForm
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
    return redirect('/')


def contactUs(request):
    contact = Contact.objects.all()
    form = ContactForm(initial={'contact': contact})
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

    context={'form': form}
    return render(request, 'abstract/contact.html', context)


def home(request):
    context = {}
    return render(request, 'abstract/home.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'reviewer'])
def abstract(request):
    abstracts = Abstract.objects.all()
    # presentation_types = Abstract.presentation_preference.all()
    # topics = Topic.objects.all()
    # presentations = Presentation_type.objects.all()
    context = {'abstracts': abstracts}
    return render(request, 'abstract/abstract.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['author', 'reviewer'])
def author(request, pk):
    author_instance = Author.objects.get(id=pk)
    abstracts = Abstract.objects.filter(author=author_instance)
    
    # Retrieve abstract information including topics
    abstract_info = []
    for abstract in abstracts:
        topics = abstract.topics.all() 
        topic_names = [topic.topics for topic in topics]  # Extract names of topics
        abstract_info.append({
            'id': abstract.id,
            'title': abstract.title,
            'topics': topic_names,
            'status': abstract.status,
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
    # status = Statuse.objects.all()

    total_author = authors.count()
    total_abstract = abstracts.count()
    accepted = abstracts.filter(status='Accepted').count

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
    # status = Statuse.objects.all()

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
    if request.method == "POST":
        form =AbstractForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.groups.filter(name='reviewer').exists():
                return redirect('/reviewer')
            elif request.user.groups.filter(name='author').exists():
                return redirect('/user')
            elif request.user.groups.filter(name='editor').exists():
                return redirect('/editor')

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
            if request.user.groups.filter(name='reviewer').exists():
                return redirect('/reviewer')
            elif request.user.groups.filter(name='author').exists():
                return redirect('/user')
            elif request.user.groups.filter(name='editor').exists():
                return redirect('/editor')
        
    context = {'form': form}
    return render(request, 'abstract/abstract_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'author', 'reviewer'])
def deleteAbstract(request, pk):
    abstract = Abstract.objects.get(id=pk)
    if request.method == "POST":
        abstract.delete()
        if request.user.groups.filter(name='reviewer').exists():
            return redirect('/reviewer')
        elif request.user.groups.filter(name='author').exists():
            return redirect('/user')
        elif request.user.groups.filter(name='editor').exists():
                return redirect('/editor')
    context ={'item': abstract}
    return render(request, 'abstract/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'author', 'reviewer'])
def userPage(request):
    author = request.user.author
    aus = request.user.author.abstract_set.all()
    
    abstracts = Abstract.objects.all()
    authors = Author.objects.all()
    # abstracts = Abstract.objects.all()

    total_author = authors.count()
    total_abstract = abstracts.count()
    accepted = abstracts.filter(status='Accepted').count

    context ={'aus':aus, 'abstracts':abstracts, 'authors': authors, 
               'total_author':total_author, 'total_abstract':total_abstract,
               'accepted': accepted, 'author':author}

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





# def assign_editors(request, abstract_id):
#     abstract = Abstract.objects.get(pk=abstract_id)
#     editors = User.objects.filter(groups__name='Editors')
#     abstracts = Abstract.objects.all()

#     if request.method == 'POST':
#         form = AssignEditorsForm(request.POST)
#         if form.is_valid():
#             editors_selected = form.cleaned_data['Editors']
#             for editor in editors_selected:
#                 abstract.editors.add(editor)
#             return redirect('/reviewer')  # Redirect to editor dashboard after assignment
#     else:
#         form = AssignEditorsForm()

#     return render(request, 'abstract/assign_editors.html', {'form': form, 'editors': editors, 'abstracts':abstracts})