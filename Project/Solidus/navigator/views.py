from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Pizzaroni, Wildberries
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity
#from .parser import parse_website_data
import json
from django.conf import settings
import os
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    parsed_datas = Pizzaroni.objects.all()[:24]
    market_datas = Wildberries.objects.all()[:24]
    
    
    form = SearchForm()
    query = None
    pizza_results = []
    market_results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A')+SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            pizza_results = Pizzaroni.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
            market_results = Wildberries.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
    
    
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
                 'market_datas':market_datas,
                 'form':form, 
                 'query':query,
                 'market_results':market_results,
                 'pizza_results':pizza_results,})


def pizzaroni_detail(request, id, slug):
    parsed_data = get_object_or_404(Pizzaroni, id=id, slug=slug)
    
    cart_product_form = CartAddProductForm()
    
    form = SearchForm()
    query = None
    pizza_results = []
    market_results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A')+SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            pizza_results = Pizzaroni.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
            market_results = Wildberries.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'navigator/product/pizzaroni_detail.html', {'parsed_data':parsed_data,
                                                                  'form':form, 
                                                                  'query':query,
                                                                  'market_results':market_results,
                                                                  'pizza_results':pizza_results,
                                                                  'cart_product_form':cart_product_form})

def wildberries_detail(request, id, product_id):
    market_data = get_object_or_404(Wildberries, id=id, product_id=product_id)
    photo_count = market_data.photo_count
    
    cart_product_form = CartAddProductForm()
    
    form = SearchForm()
    query = None
    pizza_results = []
    market_results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A')+SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            pizza_results = Pizzaroni.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
            market_results = Wildberries.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
    
    return render(request, 'navigator/product/wildberries_detail.html', {'market_data':market_data, 
                                                                  'range':range(0, int(photo_count)),
                                                                  'form':form, 
                                                                  'query':query,
                                                                  'market_results':market_results,
                                                                  'pizza_results':pizza_results,
                                                                  'cart_product_form':cart_product_form})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, 
                                slug=slug,
                               available = True)
    
    cart_product_form = CartAddProductForm()
    
    form = SearchForm()
    query = None
    pizza_results = []
    market_results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A')+SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            pizza_results = Pizzaroni.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
            market_results = Wildberries.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
    
    return render(request, 'navigator/product/product_detail.html', {'product':product,
                                                                  'form':form, 
                                                                  'query':query,
                                                                  'market_results':market_results,
                                                                  'pizza_results':pizza_results,
                                                                  'cart_product_form':cart_product_form})

    
def pizza_products(request):
        parsed_datas = Pizzaroni.objects.all()
        
        form = SearchForm()
        query = None
        pizza_results = []
        market_results = []
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_vector = SearchVector('title', weight='A')+SearchVector('body', weight='B')
                search_query = SearchQuery(query)
                pizza_results = Pizzaroni.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
                market_results = Wildberries.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
        
        return render(request, 'navigator/product/pizza_products.html', {'parsed_datas':parsed_datas,
                                                                  'form':form, 
                                                                  'query':query,
                                                                  'market_results':market_results,
                                                                  'pizza_results':pizza_results,})

def market_products(request):
        market_datas = Wildberries.objects.all()
        
        form = SearchForm()
        query = None
        pizza_results = []
        market_results = []
        if 'query' in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_vector = SearchVector('title', weight='A')+SearchVector('body', weight='B')
                search_query = SearchQuery(query)
                pizza_results = Pizzaroni.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
                market_results = Wildberries.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
        
        
        return render(request, 'navigator/product/market_products.html', {'market_datas':market_datas,
                                                                  'form':form, 
                                                                  'query':query,
                                                                  'market_results':market_results,
                                                                  'pizza_results':pizza_results,})
    
