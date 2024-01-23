from django.db import models
from navigator.models import Pizzaroni, Wildberries
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class Order(models.Model):
	phone_number = models.CharField(max_length=17)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(blank=True, null=True)
	address = models.CharField(max_length=250)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return f'Order {self.id}'

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items',
							 on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	price = models.DecimalField(max_digits=10, decimal_places=0)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return str(self.id)

	def get_cost(self):
		return self.price*self.quantity