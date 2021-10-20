from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from wardrobe.functions import *
import json

from wardrobe.models import *
from .serializers import *
from wardrobe.algorithm import *
# Create your views here.

@api_view(['GET'])
def AllClothes(request):
    clothes = Photos.objects.filter(user=request.user)
    data = ItemSerializer(clothes, many=True)

    return Response(data.data)

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
    data = org
    data['image'] = image

    item = ItemSerializer(data=data)
    if item.is_valid(raise_exception=True):
        item.save()
    return Response(item.data)

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

################ Reccomendations
@api_view(['GET'])
def reccomend(request):
    user = request.user
    items = Photos.objects.filter(user=user)
    ######### FIlTERING BY STYLES ##########
    seed = 11
    outfits = []
    for i in range(5):
        outfit = make_outfit(seed, items)
        outfits.append(outfit)

    data = json.dumps(outfits)
    return Response(data)
