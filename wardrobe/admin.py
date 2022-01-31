from django.contrib import admin

# Register your models here.
from .models import *

class TermAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']

class OutfitAdmin(admin.ModelAdmin):
    pass

class GenderAdmin(admin.ModelAdmin):
    pass

class PhotosAdmin(admin.ModelAdmin):
    list_display = ['admin_photo', 'user','description', 'category',]
    list_filter = ['user', 'style', 'category']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'admin_photo']

class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'message']

class PinAdmin(admin.ModelAdmin):
    list_display = ['image', 'Inspiration']
    list_filter = ['Inspiration']

admin.site.register(Category)
admin.site.register(Style)
admin.site.register(Occassion)
admin.site.register(Gender, GenderAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(Outfit, OutfitAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(FeedBack, FeedBackAdmin)
admin.site.register(Inspiration)
admin.site.register(Pin, PinAdmin)
# admin.site.register(Topping)
