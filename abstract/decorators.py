from django.http import HttpResponse
from django.shortcuts import redirect, render

def unautheticated_user(view_func):
    """
    Decorator that redirects authenticated users to the home page.

    Args:
        view_func: The view function to be decorated.

    Returns:The decorated view function.
    """
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    """
    Decorator that restricts access to views based on user roles.

    Args:
        allowed_roles (list, optional): A list of allowed user roles. Defaults to [].

    Returns:The decorated view function.
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return  view_func(request, *args, **kwargs)
            else:
                return render(request, 'abstract/authorize.html')
        return wrapper_func
    return decorator


def admin_only(view_func):
    """
    Decorator that restricts access to views only for users in the 'admin' group.

    Args:
        view_func (callable): The view function to be decorated.

    Returns:The decorated view function.
    """
    def wrapper_func(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'editor':
            return redirect('user-page')
        
        if group == 'author':
            return redirect('user-page')
        
        if group == 'reviewer':
            return view_func(request, *args, **kwargs)
    return wrapper_func