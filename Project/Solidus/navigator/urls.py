from django.urls import path
from . import views

app_name = 'navigator'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.pizza_detail, name='pizza_detail'),
    path('<int:id>/<slug:slug>/', views.market_detail, name='market_detail'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]