from django.contrib import admin

# Register your models here.
from .models import Photos, Category, Outfit


class OutfitAdmin(admin.ModelAdmin):
    pass

class PhotosAdmin(admin.ModelAdmin):
    list_display = ['admin_photo','description', 'category']


admin.site.register(Category)
admin.site.register(Photos, PhotosAdmin)
admin.site.register(Outfit, OutfitAdmin)

# admin.site.register(Pizza)
# admin.site.register(Topping)
