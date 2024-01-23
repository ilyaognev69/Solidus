from django.db import models
from account.models import PhoneUser
from navigator.models import Pizzaroni, Wildberries
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class CartModel(models.Model):
	phone_user = models.OneToOneField(PhoneUser, on_delete=models.CASCADE, related_name='cart')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Cart of {self.phone_user.phone_number}"

class CartItem(models.Model):
	cart = models.ForeignKey(CartModel, related_name='items', on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=0)
	old_price = models.DecimalField(max_digits=10,
									decimal_places=0, null=True)

	def __str__(self):
		return f"{self.quantity} of {self.content_object.title}"

	@property
	def total_price(self):
		return self.quantity * self.price 
	
	@property
	def total_price_for_old(self):
		return self.quantity * self.old_price 
