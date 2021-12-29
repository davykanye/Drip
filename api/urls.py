from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', views.SignUp, name='SignUp'),
    path('token/', TokenObtainPairView.as_view(), name='token'), ###
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'), ###
    path('closet/', views.AllClothes, name='closet'), ###
    path('outfits/', views.AllOutfits, name='outfits'), ###
    path('styles/', views.AllStyles, name='styles'),
    path('create_style/', views.create_style, name='create_style'),
    path('item/<str:pk>/', views.detail, name='detail'), ###
    path('create_item/', views.create_item, name='create'), ###
    path('outfit/<str:pk>/', views.outfit_detail, name='outfit_detail'), ###
    path('pinterest/<slug:search>/', views.Pinterest, name="pinterest"), 
    path('ItemScraper/<slug:search>/', views.ItemScraper, name='ItemScraper'),
    path('recommendations/', views.recommend, name='recommendations')
 
]
