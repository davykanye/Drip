from rest_framework import serializers
from django.contrib.auth.models import User
from wardrobe.models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'


class OutfitSerializer(serializers.Serializer):
    # headwear = ItemSerializer(many=False)
    top = ItemSerializer(many=False)
    lower = ItemSerializer(many=False)
    shoes = ItemSerializer(many=False)

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = '__all__'
