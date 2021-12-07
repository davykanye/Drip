from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from wardrobe.functions import *
import json

from wardrobe.models import *
from .serializers import *
from wardrobe.algorithm import *
from wardrobe.ItemDetector import *
from wardrobe.scrapers import *
# Create your views here.

@api_view(['GET'])
def AllClothes(request):
    try:
        clothes = Photos.objects.filter(user=request.user)
        data = ItemSerializer(clothes, many=True)

        return Response(data.data)
    except:
        return Response('You are not authorized')

# @api_view(['GET'])
# def reccomend(request):
#     items = Photos.objects.filter(user=request.user)
#
#     return outfit

@api_view(['GET'])
def detail(request, pk):
    photo = Photos.objects.get(id=pk)

    data = ItemSerializer(photo, many=False)

    return Response(data.data)

@api_view(['POST'])
def create_item(request):
    org = request.data
    image = search_item(org['image'])
    data = org.copy()
    data['image'] = image[0]
    category = predict(data['term'])

    try:
        photo = Photos.objects.create(
            user = request.user,
            category = Category.objects.get(name=category),
            description=data['description'],
            image=data["image"],
        )

        photo.style.set(data['style'])
        print('success')
    except Exception as e:
        print('Error is:', e)
        return Response('Error is:' + str(e))

    return Response("Success")

@api_view(['GET'])
def AllStyles(request):
    styles = Style.objects.all()
    data = StyleSerializer(styles, many=True)

    return Response(data.data)

@api_view(['POST'])
def create_style(request):
    data = StyleSerializer(data=request.data)
    if data.is_valid(raise_exception=True):
        data.save()

    return Response(data.data)

@api_view(['GET'])
def AllOutfits(request):
    clothes = Outfit.objects.filter(user=request.user)
    data = OutfitSerializer(clothes, many=True)

    return Response(data.data)

@api_view(['GET'])
def outfit_detail(request, pk):
    outfit = Outfit.objects.get(id=pk)

    data = OutfitSerializer(outfit, many=False)

    return Response(data.data)

################## Scrapers ###############
@api_view(['GET'])
def Pinterest(request, search):
    images = pinterest_scraper(search)
    data = json.dumps(images)

    return Response(data)

@api_view(['GET'])
def ItemScraper(request, search):
    images = item_scraper(search)
    data = json.dumps(images)

    return Response(data)


################ Reccomendations ###########
@api_view(['GET'])
def recommend(request):
    user = request.user
    items = Photos.objects.filter(user=user)
    ######### FIlTERING BY STYLES ##########
    seeds = pick_seeds(items)
    outfits = []
    for key, value in seeds.items():
        seed =  random.choice(value).id
        outfit = make_outfit(seed, items)
        outfit.update({"Occassion": key})
        outfits.append(outfit)

    # data = ItemSerializer(outfits, many=True)
    return Response(outfits)
