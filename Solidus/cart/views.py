from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from navigator.models import Pizzaroni, Wildberries
from navigator.forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity
from functools import wraps
# Create your views here.

def verification_required(view_func):
	@wraps(view_func)
	def _wrapped_view(request, *args, **kwargs):
		if not request.session.get('is_profiled'):
			return redirect('account:handle_phone_number_submission')  # Перенаправляем на страницу верификации
		return view_func(request, *args, **kwargs)
	return _wrapped_view



@verification_required
@require_POST
def cart_add_pizzaroni(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Pizzaroni, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@verification_required
@require_POST
def cart_add_wildberries(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Wildberries, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@verification_required
@require_POST
def cart_remove_pizzaroni(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Pizzaroni, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@verification_required
@require_POST
def cart_remove_wildberries(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Wildberries, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@verification_required
def cart_detail(request):
	cart = Cart(request)
	pizzaroni_cart = cart.get_pizzaroni_items()
	total_price_pizzaroni = sum(item.total_price for item in pizzaroni_cart)
	total_price_for_old_pizzaroni = sum(item.total_price_for_old for item in pizzaroni_cart)
	wildberries_cart = cart.get_wildberries_items()
	total_price_wildberries = sum(item.total_price for item in wildberries_cart)
	total_price_for_old_wildberries = sum(item.total_price_for_old for item in wildberries_cart)

	pizzaroni_items = []
	for item in pizzaroni_cart:
		add_form = CartAddProductForm(initial={
			'quantity':item.quantity,
			'override':True
		})
		pizzaroni_items.append((item, add_form))
		
	wildberries_items = []
	for item in wildberries_cart:
		add_form = CartAddProductForm(initial={
			'quantity':item.quantity,
			'override':True
		})
		wildberries_items.append((item, add_form))


	form = SearchForm()
	query = None
	pizza_results = []
	market_results = []
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			pizza_results = Pizzaroni.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
			market_results = Wildberries.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')

	return render(request, 'cart/detail.html', {'wildberries_items':wildberries_items,
												'total_price_wildberries':total_price_wildberries,
												'total_price_for_old_wildberries':total_price_for_old_wildberries,
												'pizzaroni_items':pizzaroni_items,
												'total_price_pizzaroni':total_price_pizzaroni,
												'total_price_for_old_pizzaroni':total_price_for_old_pizzaroni,
											   'form':form,
											   'query':query,
											   'pizza_results':pizza_results,
											   'market_results':market_results})