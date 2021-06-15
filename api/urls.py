from django.urls import path
from . import views

urlpatterns = [
    path('closet/', views.AllClothes, name='closet'),

]
