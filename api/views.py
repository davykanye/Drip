from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def AllClothes(request):
    return JsonResponse('API Things', safe=False)
