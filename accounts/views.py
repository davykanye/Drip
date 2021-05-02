from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.shortcuts import (get_object_or_404, HttpResponseRedirect)
from django.urls import reverse
import requests

# Create your views here.
def register(request):

    if request.method == 'POST':
        data = request.POST
        username = data['username']
        email = data['email']
        password = data['password1']

        if data['password1'] == data['password2']:
            if User.objects.filter(username=username).exists():
                print('username taken')
            elif User.objects.filter(email=email).exists():
                print('email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password,)
                user.save()
                auth.login(request, user)
                print('user created')
                return redirect('gallery')


        else:
            print('passwords are not matching')
            return redirect('register')

    template_name = 'accounts/register.html'
    return render(request, template_name)


def login(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('gallery')
        else:
            print('Invalid info')
            return redirect('/')


    template_name = 'accounts/login.html'
    return render(request, template_name)


def logout(request):
    auth.logout(request)
    return redirect('gallery')
