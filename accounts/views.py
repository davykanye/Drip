from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import (get_object_or_404, HttpResponseRedirect)
from accounts.forms import (EditProfileForm)
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
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
                messages.info(request, 'username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password,)
                user.save()
                auth.login(request, user)
                print('user created')
                return redirect('gallery')


        else:
            messages.info(request, 'passwords are not matching')
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
            messages.info(request, 'Username or Password is invalid')
            return redirect('/')


    template_name = 'accounts/login.html'
    return render(request, template_name)

def profile(request):
    form = EditProfileForm(request.POST, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = EditProfileForm(instance=request.user)

        context = {'form': form}
        template_name = 'wardrobe/Profile.html'
        return render(request, template_name, context)

def logout(request):
    auth.logout(request)
    return redirect('gallery')
