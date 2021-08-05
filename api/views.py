from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from wardrobe.models import *
from .serializers import *
from wardrobe.algorithm import *
# Create your views here.

@api_view(['GET'])
def AllClothes(request):

    clothes = Photos.objects.all()
    data = ItemSerializer(clothes, many=True)

    return Response(data.data)

@api_view(['GET'])
def reccomend(request):
    user = request.user
    items = Photos.objects.filter(user=user)
