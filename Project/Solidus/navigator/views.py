from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Pizza, Market
#from .parser import parse_website_data
import json
from django.conf import settings
import os

def product_list(request, category_slug=None):
    parsed_datas = Pizza.objects.all()
    market_datas = Market.objects.all()
    
    
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'navigator/product/product.html', 
                 {'category':category,
                 'categories':categories,
                 'products':products,
                 'parsed_datas':parsed_datas,
                 'market_datas':market_datas})


def pizza_detail(request, id, slug):
    parsed_data = get_object_or_404(Pizza, id=id, slug=slug)
    return render(request, 'navigator/product/pizza_detail.html', {'parsed_data':parsed_data})

def market_detail(request, id, slug):
    market_data = get_object_or_404(Market, id=id, slug=slug)
    return render(request, 'navigator/product/market_detail.html', {'market_data':market_data})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, 
                                slug=slug,
                               available = True)
    return render(request, 'navigator/product/product_detail.html', {'product':product})

    