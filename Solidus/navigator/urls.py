from django.urls import path
from . import views

app_name = 'navigator'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('market_products/', views.market_products, name='market_products'),
    path('pizza_products/', views.pizza_products, name='pizza_products'),
    path('market/<int:id>/<slug:slug>/', views.wildberries_detail, name='wildberries_detail'),
    path('pizza/<int:id>/<slug:slug>/', views.pizzaroni_detail, name='pizzaroni_detail'),
]