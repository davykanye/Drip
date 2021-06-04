from django.shortcuts import render, redirect
from wardrobe.models import Category, Style, Photos, Outfit, Occassion, Profile
from django.shortcuts import (get_object_or_404, HttpResponseRedirect)
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
import os
import json
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import requests
import random

# Create your views here.
@login_required
def gallery(request):
    user = request.user
    global prenup
    def prenup():
        try:
            pro = Profile.objects.get(user=request.user)
            profile = pro.image.url
        except ObjectDoesNotExist:
            profile = None
        return profile

    profile = prenup()
    categories = Category.objects.all()
    photos = Photos.objects.filter(user=user)
    category = request.GET.get('category')
    if category == None:
        pass
    else:
        photos = photos.filter(category__name=category)



    outfits = Outfit.objects.filter(user=user)

    context = {'categories': categories, 'photos': photos, 'outfits': outfits, 'user': user, 'profile': profile}
    template_name = 'wardrobe/wardrobe.html'
    return render(request, template_name, context)

# adding clothe items
@login_required
def add_pic(request):
    categories = Category.objects.all()
    styles = Style.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        print(type(image))
        print(image)

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        else:
            category = None

        photo = Photos.objects.create(
            user = request.user,
            category = category,
            description=data['description'],
            image=image,
        )
        return redirect('gallery')

    context = {'categories': categories, 'styles': styles}
    template_name = 'wardrobe/add_pic.html'
    return render(request, template_name, context)

# viewing clothe items
@login_required
def detail(request, pk):
    photo = Photos.objects.get(id=pk)
    print(type(photo.image))
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

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        else:
            category = None

        photo.category = category
        photo.description = data['description']
        photo.save()

        return redirect('gallery')

    context = {'categories': categories, 'photo': photo}
    template_name = 'wardrobe/edit_pic.html'
    return render(request, template_name, context)


# deleting clothe items

# Profile View man
@login_required
def delete(request, pk):
    photo = Photos.objects.get(id=pk)

    photo.delete()

    return HttpResponseRedirect('/')


def settings(request):

    context = {}
    template_name = 'wardrobe/settings.html'
    return render(request, template_name, context)
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


# ################These were the two hardest views in the entire MVP###########

########### THE OUTFIT_FEED #################
@login_required
def outfit_feed(request):
    user = request.user
    items = Photos.objects.filter(user=user)
    occassions = Occassion.objects.all()
    category = Category.objects.all()
    if len(items) <= 3:
        template_name = 'wardrobe/feed_error.html'
        context = {'occassions':occassions, 'category':category}
        return render(request, template_name, context)
    else:
        ######### FIlTERING BY STYLES ###########

        event = request.GET.get('occassion')
        if event == None:
            pass
        else:
            event = Occassion.objects.get(name=str(event))
            styles = event.styles.all()

            items = items.filter(style__name__in=list(styles))
            print(items)
            print(len(items))

        head = items.filter(category__name='headwear')
        top = items.filter(category__name='top')
        jacket = items.filter(category__name='jacket')
        lower = items.filter(category__name='lower')
        shoes = items.filter(category__name='shoes')

    #  ############# PERMUTATING THE OUTFITS PROPERLY ###################
        outfits = []
        pick = [1,1,1,1,1,2,2,3,3,3]

        for i in range(8):
            rand = random.choice(pick)
            if rand == 1:
                outfit = {
                top: random.choice(top),
                lower: random.choice(lower),
                shoes: random.choice(shoes)
                }
            elif rand == 2:
                outfit = {
                jacket: random.choice(jacket),
                top: random.choice(top),
                lower: random.choice(lower),
                shoes: random.choice(shoes)
                }
            else:
                outfit = {
                head: random.choice(head),
                top: random.choice(top),
                lower: random.choice(lower),
                shoes: random.choice(shoes)
                }
            outfits.append(outfit)


        saved_outfit = request.GET.get('outfit')
        # print(saved_outfit)
        # print(type(saved_outfit))

        profile = prenup()
        context = {'outfits': outfits, 'occassions':occassions, 'category':category, 'profile':profile}
        template_name = 'wardrobe/outfit_feed.html'
        return render(request, template_name, context)



@login_required
def outfit_view(request):

    context = {}
    template_name = 'wardrobe/outfit_view.html'
    return render(request, template_name, context)

############# ADD ITEMS IN A SPECIAL WAY #####################
@login_required
def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        query = '+'.join(query.split())
    else:
        query = 'grey+shirt'

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

    description = query.split('+')
    description = ' '.join(description)

    global proper
    def proper():
        return description



    context = {'images': links, 'query': description}
    template_name = 'wardrobe/search.html'

    return render(request, template_name, context)

@login_required
def search_item(request, image):

    SAVE_FOLDER = 'staticfiles/searched'
    name = proper()
    id = random.randint(1, 99)

    categories = Category.objects.all()
    styles = Style.objects.all()

    user = request.user
    category = Category.objects.get(name='top')
    style = Style.objects.all()
    response = requests.get(image)

    photo = SAVE_FOLDER + '/' + name + str(id) + '.jpg'
    with open(photo, 'wb') as file:
        file.write(response.content)

    img = Image.open(photo)
    image_bytes = BytesIO()
    img.save(image_bytes, format='JPEG')


    hope = InMemoryUploadedFile(
    image_bytes, None, name, 'image/jpeg', None, None, None
    )


    print(type(img))
    print(img.size)

    if request.method == 'POST':
        data = request.POST
        selected_style = request.POST.getlist('style')
        styles = []
        for i in selected_style:
            i = int(i)
            styles.append(i)

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        else:
            category = None

        photo = Photos.objects.create(
            user = request.user,
            category = category,
            description=data['description'],
            image=hope,
        )
        photo.style.set(styles)

        return redirect('gallery')



    template_name = 'wardrobe/search_item.html'
    context = {'image': image, 'name': name, 'categories': categories, 'styles': styles}
    return render(request, template_name, context)
