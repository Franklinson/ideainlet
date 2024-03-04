from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import *
from .forms import AbstractForm, CreateUserForm, AuthorForm, ContactForm, PlaceOrderForm
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
    """
    Renders the registration page and handles user registration logic.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        A rendered response object for either the registration form
        or redirection to the login page upon successful registration.
    """    
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
    """
    Renders the login page and handles user authentication logic.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns: 
        A rendered response object for either the login form
        or redirection to the home page upon successful login.
    """

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
    """
    Logs out the currently authenticated user and redirects them to the home page.

    Args:
        request: The incoming HTTP request object.

    Returns:
        HttpResponse: A redirection response object to the home page.
    """
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
@allowed_users(allowed_roles=['editor', 'reviewer'])
def editor_dashboard(request):
    # Get the abstracts assigned to the logged-in editor
    assigned_abstracts = Abstract.objects.filter(editors=request.user.groups.first())
    total_abstract = assigned_abstracts.count()
    is_editor = request.user.groups.filter(name='editor').exists()


    context = {'assigned_abstracts': assigned_abstracts,
               'total_abstract':total_abstract, 'is_editor':is_editor}
    return render(request, 'abstract/editor.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'author', 'reviewer'])
def createAbstract(request, pk):
    author = Author.objects.get(id=pk)
    if request.method == "POST":
        form = AbstractForm(request.POST, request.FILES, initial={'author': author})
        if form.is_valid():
            abstract = form.save()
            redirect_url = get_redirect_url(request.user)
            return redirect(redirect_url)
    else:
        form = AbstractForm(initial={'author': author})
    context = {"form": form}
    return render(request, 'abstract/abstract_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['editor', 'author', 'reviewer'])
def updateAbstract(request, pk):
    abstract = Abstract.objects.get(id=pk)
    if request.method == 'POST':
        form = AbstractForm(request.POST, request.FILES, instance=abstract)
        if form.is_valid():
            form.save()
            redirect_url = get_redirect_url(request.user)
            return redirect(redirect_url)
    else:
        form = AbstractForm(instance=abstract)
    is_editor = request.user.groups.filter(name='editor').exists()
    context = {'form': form, 'is_editor':is_editor}
    return render(request, 'abstract/abstract_form.html', context)

def get_redirect_url(user):
    if user.groups.filter(name='reviewer').exists():
        return '/reviewer'
    elif user.groups.filter(name='author').exists():
        return '/user'
    elif user.groups.filter(name='editor').exists():
        return '/editor'
    else:
        return '/'


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
            return redirect('/user')

    context = {'form': form}
    return render(request, 'abstract/account_settings.html', context)





@allowed_users(allowed_roles=['editor', 'reviewer'])
def assign_abstract(request):
    if request.method == 'POST':
        abstract_id = request.POST.get('abstract_id')
        group_ids = request.POST.getlist('groups')
        
        abstract = Abstract.objects.get(id=abstract_id)
        groups = Group.objects.filter(id__in=group_ids)
        
        # Clear existing editor groups and assign the selected groups
        abstract.editors.clear()
        abstract.editors.add(*groups)
        
        return redirect('reviewer')

    else:
        # Filter users who belong to the 'Editor' group
        editors_group = Group.objects.get(name='editor')
        editors = editors_group.user_set.all()

        abstracts = Abstract.objects.all()
        context = {'abstracts': abstracts, 'editors': editors}
        return render(request, 'abstract/assign_abstract.html', context)
    

def place_order(request):
	if request.method == 'POST':
		form = PlaceOrderForm(request.POST)
		if form.is_valid():
			var = form.save(commit=False)
			product = Product.objects.get(pk=1)
			var.product = product
			var.user = request.user
			var.total_cost = product.price
			var.save()
			payment = Payment.objects.create(amount=var.total_cost, email=request.user.email, user=request.user)
			payment.save()
			pk = settings.PAYSTACK_PUBLIC_KEY
			context = {
			'total_cost': var.total_cost,
			# 'item_amount': var.item_amount,
			'payment': payment,
			'paystack_pub_key':pk,
			'amount_value': payment.amount_value()
			}
			request.session['order_id'] = var.id
			return render(request, 'abstract/make_payment.html', context)

		else:
			messages.warning(request, 'Error, Something went wrong')
			return redirect('place-order')

	else:
		form = PlaceOrderForm()
		context = {'form':form}
		return  render(request, 'abstract/place_order.html', context)
     

def verify_payment(request, ref):
	payment = Payment.objects.get(ref=ref)
	verified = payment.verify_payment()

	if verified:
		pk = request.session['order_id']
		order = PlaceOrder.objects.get(pk=pk)
		order.is_verified = True
		order.save()
		context = {'place-order':pk, 'payment':payment}
		return render(request, 'abstract/success.html', context)
	else:
		messages.warning(request, 'Sorry your Payment was not processed, contact admin')
		return redirect('/')