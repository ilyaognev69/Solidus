from django.db import models
import datetime
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils import timezone


class PhoneUser(models.Model):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{7,15}$')
	phone_number = models.CharField(validators=[phone_regex], max_length=17)
	code = models.CharField(max_length=6)
	created_at = models.DateTimeField(auto_now_add=True)
	attempts = models.IntegerField(default=0)

	def increment_attempts(self):
		self.attempts += 1
		self.save()

	def can_attempt(self):
		return self.attempts < 1000

	def is_valid(self):
		# Проверка, что код еще действителен (например, в течение 10 минут)
		return self.created_at >= timezone.now() - timezone.timedelta(minutes=10)
	

class Profile(models.Model):
	phone_number = models.CharField(max_length=17)
	first_name = models.CharField(max_length=20, db_index=True)
	last_name = models.CharField(max_length=20, db_index=True)
	email = models.EmailField(max_length=254, blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m?%d/', blank=True)