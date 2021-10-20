from rest_framework import serializers
from django.contrib.auth.models import User
from wardrobe.models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'


class OutfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outfit
        fields = '__all__'


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = '__all__'
