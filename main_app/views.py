from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import CatForm, LoginForm
from .models import Cat
import logging


# Create your views here.

# default view for '/index' path
def index(request):
    cats = Cat.objects.all()
    form = CatForm()
    return render(request, 'index.html', { 'cats':cats, 'form':form })

# show details for individual cat
def show(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'show.html', {'cat': cat})

# enter new cat information form
def post_cat(request):
    form = CatForm(request.POST)
    if form.is_valid:
        cat = form.save(commit = False)
        cat.user = request.user
        cat.save()
    return HttpResponseRedirect('/')

# show collection of cats that user enters
def profile(request, username):
    user = User.objects.get(username=username)
    cats = Cat.objects.filter(user=user)
    return render(request, 'profile.html', {'username': username, 'cats': cats})

# user login form
def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print("user is active")
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
                return HttpResponse('/')
            else:
                print("The username and/or password is incorrect.")
            return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout link
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

# button to 'like' a cat, show up on each cat
def like_cat(request):
    cat_id = request.GET.get('cat_id', None)

    likes = 0
    if (cat_id):
        cat = Cat.objects.get(id=int(cat_id))
        if cat is not None:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)
