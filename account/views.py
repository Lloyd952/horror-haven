from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def logout_view(request):
    """Custom logout view that allows GET requests"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('blog:post_list')
