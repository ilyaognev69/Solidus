from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('wildberries/add/<int:product_id>/', views.cart_add_wildberries, name='cart_add_wildberries'),
    path('pizzaroni/add/<int:product_id>/', views.cart_add_pizzaroni, name='cart_add_pizzaroni'),
    path('pizzaroni/remove/<int:product_id>/', views.cart_remove_pizzaroni, name='cart_remove_pizzaroni'),
    path('wildberries/remove/<int:product_id>/', views.cart_remove_wildberries, name='cart_remove_wildberries'),
]