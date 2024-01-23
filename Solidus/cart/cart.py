from decimal import Decimal
from django.conf import settings
from navigator.models import Pizzaroni, Wildberries
from account.models import PhoneUser
from .models import CartModel, CartItem
from django.contrib.contenttypes.models import ContentType


class Cart(object):
    
	def __init__(self, request):
		self.phone_number = request.session.get('phone_number')

		if self.phone_number:
			try:
				self.phone_user = PhoneUser.objects.get(phone_number=self.phone_number)
				self.cart, created = CartModel.objects.get_or_create(phone_user=self.phone_user)
			except PhoneUser.DoesNotExist:
				# Обработка ситуации, когда пользователь с таким номером телефона не найден
				self.cart = None
		else:
			# Действия, если пользователь не авторизован
			self.cart = None
			
	def get_pizzaroni_items(self):
		pizzaroni_type = ContentType.objects.get_for_model(Pizzaroni)
		return self.cart.items.filter(content_type=pizzaroni_type)
	
	def get_wildberries_items(self):
		wildberries_type = ContentType.objects.get_for_model(Wildberries)
		return self.cart.items.filter(content_type=wildberries_type)

	def add(self, product, quantity=1, override_quantity=False):
		product_type = ContentType.objects.get_for_model(type(product))
		object_id = product.id
		
		cart_item, created = CartItem.objects.get_or_create(
			cart=self.cart,
			content_type = product_type,
			object_id=object_id,
			defaults={'price': product.price,
					 'old_price': product.old_price,}  # Установка начальной цены при создании
		)

		if created:
			cart_item.price = product.price  # Установка цены для новых элементов
			cart_item.old_price = product.old_price  # Установка цены для новых элементов
		if override_quantity or created:
			cart_item.quantity = quantity
		else:
			cart_item.quantity += quantity

		cart_item.save()
		

	def remove(self, product):
		product_type = ContentType.objects.get_for_model(type(product))
		object_id = product.id
		
		CartItem.objects.filter(
						cart=self.cart,
						content_type = product_type,
						object_id=object_id
		).delete()


	def __iter__(self):
		return iter(self.cart.items.all())

	def __len__(self):
		return sum(item.quantity for item in self.cart.items.all())
	
	def total_price(self):
		return sum(item.total_price for item in self.cart.items.all())
	
	def total_price_for_old(self):
		return sum(item.total_price_for_old for item in self.cart.items.all())

	def clear(self, product_type=None):
		if product_type:
			content_type = ContentType.objects.get_for_model(product_type)
			CartItem.objects.filter(cart=self.cart, content_type=content_type).delete()
		else:
			CartItem.objects.filter(cart=self.cart).delete()