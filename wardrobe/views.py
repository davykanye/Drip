from django.shortcuts import render, redirect
from wardrobe.models import Category, Photos, Outfit, Occassion
from django.shortcuts import (get_object_or_404, HttpResponseRedirect)
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import os
import json
from bs4 import BeautifulSoup
import requests
import time
import random
import math

# Create your views here.
@login_required
def gallery(request):
    user = request.user
    categories = Category.objects.all()
    photos = Photos.objects.filter(user=user)
    outfits = Outfit.objects.all()

    context = {'categories': categories, 'photos': photos, 'outfits': outfits, 'user': user}
    template_name = 'wardrobe/wardrobe.html'
    return render(request, template_name, context)

# adding clothe items
@login_required
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
@login_required
def detail(request, pk):
    photo = Photos.objects.get(id=pk)
    context = {'photo' : photo}
    template_name = 'wardrobe/detail.html'
    return render(request, template_name, context)

# editing clothe items
@login_required
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
@login_required
def delete(request, pk):
    photo = Photos.objects.get(id=pk)

    photo.delete()

    return HttpResponseRedirect('/')


################## OUTFITS SECTION ###############################

# Creating Outfits
@login_required
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

@login_required
def outfit_feed(request):
    user = request.user
    items = Photos.objects.filter(user=user)
    ######### FIlTERING BY STYLES ###########
    occassions = Occassion.objects.all()
    category = Category.objects.all()
    event = request.GET.get('occassion')
    print(event)
    if event == None:
        pass
    else:
        event = Occassion.objects.get(name=str(event))
        styles = event.styles.all()
        print(styles)

    ####### FIlTERING BY BODYPARTS ###########
    head = items.filter(category__name='headwear')
    top = items.filter(category__name='top')
    jacket = items.filter(category__name='jacket')
    lower = items.filter(category__name='lower')
    shoes = items.filter(category__name='shoes')

#  ############# PERMUTATING THE OUTFITS PROPERLY ###################
    outfits = []

    for i in range(8):
        outfit = {
        head: random.choice(head),
        top: random.choice(top),
        lower: random.choice(lower),
        shoes: random.choice(shoes)
        }
        outfits.append(outfit)

    context = {'outfits': outfits, 'occassions':occassions, 'category':category}
    template_name = 'wardrobe/outfit_feed.html'
    return render(request, template_name, context)

@login_required
def outfit_view(request, pk):
    outfit = Outfit.objects.get(id=pk)

    context = {'outfit': outfit}
    template_name = 'wardrobe/outfit_view.html'
    return render(request, template_name, context)

############# ADD ITEMS IN A SPECIAL WAY #####################
@login_required
def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        query = '+'.join(query.split())
        print(query)
    else:
        query = 'clothes'

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


    search = GOOGLE_IMAGE + "q=" + query
    html = requests.get(search, headers=usr_agent)
    response = html.text

    soup = BeautifulSoup(response, 'html.parser')
    results = soup.find_all('img')

    links = []
    for img in results:
        link = img['src']
        links.append(link)
    links.pop(0)


    try:
        image_picked = request.GET.get('image')
        response = requests.get(image_picked)
        print(image_picked)
    except:
        pass

    # if request.method == 'POST':
    #     data = request.POST
    #     selected_clothes = request.POST.getlist('clothe')
    #
    #     for i, imagelink in enumerate(selected_clothes):
    #         response = requests.get(imagelink)
    #
    #         imagename = SAVE_FOLDER + '/' + query + str(i+1) + '.jpg'
    #         with open(imagename, 'wb') as file:
    #             file.write(response.content)
    #
    #         photo = Photos.objects.create(
    #             description='clothe engine test',
    #             image=imagename,
    #         )
    #     return redirect('gallery')

    description = query.split('+')
    description = ' '.join(description)


    context = {'images': links, 'query': description}
    template_name = 'wardrobe/search_item.html'

    return render(request, template_name, context)
