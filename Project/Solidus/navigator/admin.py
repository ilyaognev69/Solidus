from django.contrib import admin
from .models import Category, Product, Pizza, Market
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name', )}
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Pizza)
class Pizza(admin.ModelAdmin):
    list_display = ['title', 'price', 'slug']
    prepopulated_fields = {'slug':('title',)}
    
@admin.register(Market)
class Market(admin.ModelAdmin):
    list_display = ['title', 'new_price', 'slug']
