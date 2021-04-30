from django.shortcuts import render, redirect
from wardrobe.models import Category, Photos, Outfit
from django.shortcuts import (get_object_or_404, HttpResponseRedirect)
from django.urls import reverse
import os
import json
from bs4 import BeautifulSoup
import requests
import time
import random
import math

# Create your views here.

def gallery(request):
    categories = Category.objects.all()
    photos = Photos.objects.all()
    outfits = Outfit.objects.all()

    context = {'categories': categories, 'photos': photos}
    template_name = 'wardrobe/wardrobe.html'
    return render(request, template_name, context)

# adding clothe items
def add_pic(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        photo = Photos.objects.create(
            category = category,
            description=data['description'],
            image=image,
        )
        return redirect('gallery')

    context = {'categories': categories}
    template_name = 'wardrobe/add_pic.html'
    return render(request, template_name, context)

# viewing clothe items
def detail(request, pk):
    photo = Photos.objects.get(id=pk)
    context = {'photo' : photo}
    template_name = 'wardrobe/detail.html'
    return render(request, template_name, context)

# editing clothe items
def edit_pic(request, pk):
    categories = Category.objects.all()
    photo = Photos.objects.get(id=pk)

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        photo.category = category
        photo.description = data['description']
        photo.image = image
        photo.save()

        return redirect('gallery')

    context = {'categories': categories, 'photo': photo}
    template_name = 'wardrobe/edit_pic.html'
    return render(request, template_name, context)


# deleting clothe items
def delete(request, pk):
    photo = Photos.objects.get(id=pk)

    photo.delete()

    return HttpResponseRedirect('/')


################## OUTFITS SECTION ###############################

# Creating Outfits
def create_outfit(request):
    photos = Photos.objects.all()

    if request.method == 'POST':
        data = request.POST
        selected_clothes = request.POST.getlist('clothe')
        items = []
        for i in selected_clothes:
            i = int(i)
            items.append(i)

        #then create outfit in the models

        outfit_name = data['name']

        outfit = Outfit.objects.create(name = outfit_name)
        outfit.items.set(items)

        return redirect('gallery')

    context = {'photos': photos}
    template_name = 'wardrobe/create_outfit.html'

    return render(request, template_name, context)

def outfit_feed(request):
    outfits = Outfit.objects.all()
    items = Photos.objects.all()

    context = {'outfits': outfits}
    template_name = 'wardrobe/outfit_feed.html'
    return render(request, template_name, context)

def outfit_view(request, pk):
    outfit = Outfit.objects.get(id=pk)

    context = {'outfit': outfit}
    template_name = 'wardrobe/outfit_view.html'
    return render(request, template_name, context)

############# ADD ITEMS IN A SPECIAL WAY #####################
def search(request):

    SAVE_FOLDER = 'static/images'

    GOOGLE_IMAGE = \
    'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

    usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

    query = 'black+shirt'

    search = GOOGLE_IMAGE + "q=" + query
    html = requests.get(search, headers=usr_agent)
    response = html.text

    soup = BeautifulSoup(response, 'html.parser')
    results = soup.find_all('img')

    links = []
    for img in results:
        link = img['src']
        links.append(link)

    if request.method == 'POST':
        data = request.POST
        selected_clothes = request.POST.getlist('clothe')

        for i, imagelink in enumerate(selected_clothes):
            response = requests.get(imagelink)

            imagename = SAVE_FOLDER + '/' + query + str(i+1) + '.jpg'
            with open(imagename, 'wb') as file:
                file.write(response.content)

            photo = Photos.objects.create(
                description='clothe engine test',
                image=imagename,
            )
        return redirect('gallery')


    context = {'images': links}
    template_name = 'wardrobe/search_item.html'

    return render(request, template_name, context)
