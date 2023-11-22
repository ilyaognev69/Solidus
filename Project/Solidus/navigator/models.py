from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('navigator:product_list_by_category', args=[self.slug])
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', 
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length = 200, 
                            db_index=True)
    slug = models.SlugField(max_length=200, 
                            db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', 
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, 
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('navigator:product_detail', args=[self.id, self.slug])
    

class Pizza(models.Model):
    title = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=200, 
                            db_index=True, null=True)
    picture_url = models.URLField(null=True)
    url = models.URLField()
    price = models.DecimalField(max_digits=10, 
                                decimal_places=2, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('navigator:pizza_detail', args=[self.id, self.slug])
    
    
class Market(models.Model):
    title = models.CharField(max_length=255, null=True)
    product_id = models.SlugField(max_length=200, 
                            db_index=True, null=True)
    picture_urls = models.URLField(null=True)
    old_price = models.DecimalField(max_digits=10, 
    new_price = models.DecimalField(max_digits=10, 
                                decimal_places=2, null=True)
    description = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('navigator:market_detail', args=[self.id, self.slug])