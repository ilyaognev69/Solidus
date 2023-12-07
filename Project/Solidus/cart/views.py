from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .wildberries_cart import WildberriesCart
from .pizzaroni_cart import PizzaroniCart
from .forms import CartAddProductForm
from navigator.models import Category, Product, Pizzaroni, Wildberries
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from navigator.forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity

# Create your views here.


@require_POST
def cart_add_pizzaroni(request, product_id):
    cart = PizzaroniCart(request)
    product = get_object_or_404(Pizzaroni, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_add_wildberries(request, product_id):
    cart = WildberriesCart(request)
    product = get_object_or_404(Wildberries, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove_pizzaroni(request, product_id):
    cart = PizzaroniCart(request)
    pizza_product = get_object_or_404(Pizzaroni, id=product_id)
    cart.remove(pizza_product)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove_wildberries(request, product_id):
    cart = WildberriesCart(request)
    pizza_product = get_object_or_404(Wildberries, id=product_id)
    cart.remove(pizza_product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    wildberries_cart = WildberriesCart(request)
    pizzaroni_cart = PizzaroniCart(request)
    
    
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
    
    return render(request, 'cart/detail.html', {'wildberries_cart':wildberries_cart,
                                                'pizzaroni_cart':pizzaroni_cart,
                                               'form':form,
                                               'query':query,
                                               'pizza_results':pizza_results,
                                               'market_results':market_results})