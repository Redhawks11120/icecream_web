from django.shortcuts import render
from . import models
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'authentication/login.html')
    context = {
        'user': request.user,
    }
    return HttpResponseRedirect(reverse("home"))

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'authentication/login.html')
    return render(request, 'authentication/login.html')


def register_view(request):
    if request.method == 'POST':
        useremail = request.POST['useremail']
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        if password != repassword:
            return HttpResponseRedirect(reverse(index))
        elif username == '' or useremail == '' or password == '' or repassword == '':
            return HttpResponseRedirect(reverse(index))
        user = User.objects.create_user(username= username,email=useremail,password= password)
        user.save()
        authenticate(request, username=username, password=password)
        return HttpResponseRedirect(reverse("home"))
    return render(request, 'authentication/register.html')

def logout_view(request):

    if not request.user.is_authenticated:
        return render(request, "authentication/login.html")
    logout(request)
    return HttpResponseRedirect(reverse("login"))