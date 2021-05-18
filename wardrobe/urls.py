from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('add/', views.add_pic, name='add_pic'),
    path('photo/<str:pk>/', views.detail, name='photo'),
    path('update/<str:pk>/', views.edit_pic, name='edit_pic'),
    path('delete/<str:pk>/', views.delete, name='delete'),
    path('outfit/', views.create_outfit, name='create_outfit'),
    path('outfit_feed/', views.outfit_feed, name='outfit_feed'),
    path('outfit_view/', views.outfit_view, name='outfit_view'),
    path('search/', views.search, name='search'),
    path('test/<path:image>/', views.search_item, name='search_item')
]
