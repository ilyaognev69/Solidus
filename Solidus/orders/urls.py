from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
  path('wildberries/', views.order_create_wildberries, name='order_create_wildberries'),
  path('pizzaroni/', views.order_create_pizzaroni, name='order_create_pizzaroni'),
]