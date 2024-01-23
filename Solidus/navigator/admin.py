from django.contrib import admin
from .models import Pizzaroni, Wildberries, Ozon
# Register your models here.

@admin.register(Pizzaroni)
class Pizzaroni(admin.ModelAdmin):
    list_display = ['title', 'price', 'slug']
    prepopulated_fields = {'slug':('title',)}
    
@admin.register(Wildberries)
class Wildberries(admin.ModelAdmin):
    list_display = ['title', 'price', 'slug']

@admin.register(Ozon)
class Ozon(admin.ModelAdmin):
    list_display = ['title', 'price', 'slug']
