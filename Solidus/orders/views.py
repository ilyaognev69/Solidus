from django.shortcuts import render, get_object_or_404
from navigator.models import Pizzaroni, Wildberries
from navigator.forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from functools import wraps
from account.models import Profile
from django.contrib.contenttypes.models import ContentType


def verification_required(view_func):
	@wraps(view_func)
	def _wrapped_view(request, *args, **kwargs):
		if not request.session.get('is_profiled'):
			return redirect('account:handle_phone_number_submission')  # Перенаправляем на страницу верификации
		return view_func(request, *args, **kwargs)
	return _wrapped_view

@verification_required
def order_create_wildberries(request):
	
	form = SearchForm()
	query = None
	result = []
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			result = Product.objects.annotate(similarity=TrigramSimilarity('name', query)).filter(similarity__gt=0.1).order_by('-similarity')
	
	
	phone_number = request.session.get('phone_number')
	profile = get_object_or_404(Profile, phone_number=phone_number)
	cart = Cart(request) #here is cart
	wildberries_cart = cart.get_wildberries_items()
	total_price_wildberries = sum(item.total_price for item in wildberries_cart)
	order_form = OrderCreateForm(request.POST)
	if order_form.is_valid():
		address = order_form.cleaned_data['address']
		order = Order.objects.create(phone_number=profile.phone_number, first_name=profile.first_name, last_name=profile.last_name, email=profile.email, address=address)
		for item in wildberries_cart:
			OrderItem.objects.create(order=order, content_type=ContentType.objects.get_for_model(Wildberries),
								object_id=item.id,
								price=item.price, quantity=item.quantity)

		cart.clear(product_type=Wildberries)
		return render(request, 'orders/order/created.html', {'order':order,
															'form':form,
														   'query':query,
														   'result':result,})

	return render(request, 'orders/order/wildberries_create.html', {'wildberries_cart':wildberries_cart,
														'total_price_wildberries':total_price_wildberries,
														'order_form':order_form,
													   'form':form,
													   'query':query,
													   'result':result,})

@verification_required
def order_create_pizzaroni(request):
	
	form = SearchForm()
	query = None
	result = []
	if 'query' in request.GET:
		form = SearchForm(request.GET)
		if form.is_valid():
			query = form.cleaned_data['query']
			result = Product.objects.annotate(similarity=TrigramSimilarity('name', query)).filter(similarity__gt=0.1).order_by('-similarity')
	
	
	phone_number = request.session.get('phone_number')
	profile = get_object_or_404(Profile, phone_number=phone_number)
	cart = Cart(request) #here is cart
	pizzaroni_cart = cart.get_pizzaroni_items()
	total_price_pizzaroni = sum(item.total_price for item in pizzaroni_cart)
	order_form = OrderCreateForm(request.POST)
	if order_form.is_valid():
		address = order_form.cleaned_data['address']
		order = Order.objects.create(phone_number=profile.phone_number, first_name=profile.first_name, last_name=profile.last_name, email=profile.email, address=address)
		for item in pizzaroni_cart:
			OrderItem.objects.create(order=order, content_type=ContentType.objects.get_for_model(Pizzaroni),
								object_id=item.id,
								price=item.price, quantity=item.quantity)

		cart.clear(product_type=Pizzaroni)
		return render(request, 'orders/order/created.html', {'order':order,
															'form':form,
														   'query':query,
														   'result':result,})

	return render(request, 'orders/order/pizzaroni_create.html', {'pizzaroni_cart':pizzaroni_cart, 
														'total_price_pizzaroni':total_price_pizzaroni,
														'order_form':order_form,
													   'form':form,
													   'query':query,
													   'result':result,})