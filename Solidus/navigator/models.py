from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
# Create your models here.
    

class Pizzaroni(models.Model):
	title = models.CharField(max_length=255, null=True)
	slug = models.SlugField(max_length=200, 
							db_index=True, null=True)
	picture_url = models.URLField(null=True)
	old_price = models.DecimalField(max_digits=10,
									decimal_places=0, null=True)
	price = models.DecimalField(max_digits=10, 
								decimal_places=2, null=True)
	description = models.TextField(blank=True, null=True)
	website = models.CharField(max_length=100, null=True)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('navigator:pizzaroni_detail', args=[self.id, self.slug])
    
    
class Wildberries(models.Model):
	title = models.CharField(max_length=255, null=True)
	slug = models.SlugField(max_length=200, 
							db_index=True, null=True)
	picture_urls = ArrayField(models.CharField(max_length=200), null=True)
	old_price = models.DecimalField(max_digits=10,
									decimal_places=0, null=True)
	price = models.DecimalField(max_digits=10, 
								decimal_places=0, null=True)
	reviewRating = models.DecimalField(max_digits=10, 
								decimal_places=1, null=True)
	description = models.TextField(blank=True, null=True)
	website = models.CharField(max_length=100, null=True)
	photo_count = models.DecimalField(max_digits=10, decimal_places=0, null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('navigator:wildberries_detail', args=[self.id, self.slug])
	

class Ozon(models.Model):
	title = models.CharField(max_length=255, null=True)
	slug = models.SlugField(max_length=200, 
							db_index=True, null=True)
	picture_urls = ArrayField(models.CharField(max_length=200), null=True)
	old_price = models.DecimalField(max_digits=10,
									decimal_places=0, null=True)
	price = models.DecimalField(max_digits=10, 
								decimal_places=0, null=True)
	reviewRating = models.DecimalField(max_digits=10, 
								decimal_places=1, null=True)
	description = models.TextField(blank=True, null=True)
	website = models.CharField(max_length=100, null=True)
	photo_count = models.DecimalField(max_digits=10, decimal_places=0, null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('navigator:ozon_detail', args=[self.id, self.slug])