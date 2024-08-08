from django.shortcuts import redirect
from django.contrib import messages

def user_not_logged_in(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "You are already registered and logged in")
            return redirect('account:user_dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func