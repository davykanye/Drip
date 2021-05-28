from django.contrib import admin

# Register your models here.
from .models import *


class OutfitAdmin(admin.ModelAdmin):
    pass

class PhotosAdmin(admin.ModelAdmin):
    list_display = ['admin_photo', 'user','description', 'category']
    list_filter = ['user', 'style', 'category']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'admin_photo']


admin.site.register(Category)
admin.site.register(Style)
admin.site.register(Occassion)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(Outfit, OutfitAdmin)
admin.site.register(Profile, ProfileAdmin)
# admin.site.register(Topping)
