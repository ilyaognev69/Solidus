from django.urls import path
from . import views

app_name = 'navigator'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('market_products/', views.market_products, name='market_products'),
    path('pizza_products/', views.pizza_products, name='pizza_products'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('market/<int:id>/<slug:product_id>/', views.wildberries_detail, name='wildberries_detail'),
    path('pizza/<int:id>/<slug:slug>/', views.pizzaroni_detail, name='pizzaroni_detail'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]