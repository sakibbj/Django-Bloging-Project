from django.shortcuts import render, redirect
from blogs.models import Category, Blog
from assignments.models import About
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def home(request):
    featured_posts = Blog.objects.filter(is_featured=True, status='Published').order_by('updated_at')
    posts = Blog.objects.filter(is_featured=False, status='Published')

    try:
        about = About.objects.get()
    except:
        about = None

    context = {
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about,
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        forms = RegistrationForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('register')
        else:
            print(forms.errors)
    else:
        forms = RegistrationForm()
    context = {
        'forms': forms, 
    }
    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        forms = AuthenticationForm(request, request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
            return redirect('dashboard')
    forms = AuthenticationForm()
    context = {
        'forms': forms,
    }
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('home')