from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['order']
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'phone_number', 'first_name', 'last_name', 'email', 'address','paid', 'created', 'updated']
	list_filter = ['paid', 'created', 'updated']
	inlines = [OrderItemInline]