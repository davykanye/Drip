from rest_framework import serializers
from django.contrib.auth.models import User
from wardrobe.models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photos
        fields = '__all__'
