from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.shortcuts import (get_object_or_404, HttpResponseRedirect)
from django.urls import reverse
import requests

# Create your views here.
def register(request):

    # if request.method == 'POST':
    #     data = request.POST
    #
    #
    #     user = User.objects.create_user()

    template_name = 'accounts/register.html'
    return render(request, template_name)


def login(request):
    pass

def logout(request):
    pass
