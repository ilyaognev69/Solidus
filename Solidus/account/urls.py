from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'

urlpatterns = [
	path('handle_phone_number_submission/', views.handle_phone_number_submission, name='handle_phone_number_submission'),
	path('verify_code/', views.verify_code, name='verify_code'),
	path('profile_detail/', views.profile_detail, name='profile_detail'),
	path('logout/', views.logout, name='logout'),
	path('edit_profile/', views.edit_profile, name='edit_profile'),
	path('profile_view/', views.profile_view, name='profile_view'),
]