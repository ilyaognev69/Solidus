from django.contrib import admin
from .models import Profile, PhoneUser
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'phone_number', 'email', 'photo']
	
@admin.register(PhoneUser)
class PhoneUserAdmin(admin.ModelAdmin):
	list_display = ['phone_number', 'code']