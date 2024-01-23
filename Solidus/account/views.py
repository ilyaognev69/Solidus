from django.shortcuts import render, redirect, get_object_or_404
from navigator.models import Pizzaroni, Wildberries
from navigator.forms import SearchForm
from django.contrib.postgres.search import TrigramSimilarity
import random
import os
from twilio.rest import Client
from django.conf import settings
from .models import PhoneUser, Profile
from .forms import PhoneNumberForm, VerificationCodeForm, ProfileEditForm, EditProfileForm
from twilio.rest import Client
from functools import wraps
from django.utils import timezone

def verification_required(view_func):
	@wraps(view_func)
	def _wrapped_view(request, *args, **kwargs):
		if not request.session.get('is_profiled'):
			return redirect('account:handle_phone_number_submission')  # Перенаправляем на страницу верификации
		return view_func(request, *args, **kwargs)
	return _wrapped_view

def verification_required_for_profile(view_func):
	@wraps(view_func)
	def _wrapped_view(request, *args, **kwargs):
		if not request.session.get('is_verified'):
			return redirect('account:handle_phone_number_submission')  # Перенаправляем на страницу верификации
		return view_func(request, *args, **kwargs)
	return _wrapped_view

def generate_random_code():
    return str(random.randint(100000, 999999))

def handle_phone_number_submission(request):

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

	number_form = PhoneNumberForm(request.POST)
	if number_form.is_valid():
		phone_number = number_form.cleaned_data['phone_number']
		code = generate_random_code()
		try:
			phone_user = PhoneUser.objects.get(phone_number=phone_number)
			phone_user.code = code  # Обновить код для существующего пользователя
			phone_user.created_at = timezone.now()
			phone_user.save()
		except PhoneUser.DoesNotExist:
			# Если пользователя нет, создать нового
			phone_user = PhoneUser.objects.create(phone_number=phone_number, code=code)


		client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

	#		message = client.messages.create(
	#			body=f"Ваш код подтверждения: {code}",
	#			from_="+18452592620",
	#			to="+79190274350"
	#		)
		request.session['phone_number'] = phone_number
		return redirect('account:verify_code')
	return render(request, 'account/handle_phone_number_submission.html', {'number_form':number_form,
																		  'form':form,
																		   'query':query,
																		   'pizza_results':pizza_results,
											   'market_results':market_results})
		
def verify_code(request):
	
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

	verify_form = VerificationCodeForm(request.POST)
	if verify_form.is_valid():
		v_code = verify_form.cleaned_data['code']
		phone_number = request.session.get('phone_number')
		try:
			verification = PhoneUser.objects.get(phone_number=phone_number, code=v_code)
		except PhoneUser.DoesNotExist:
			# Верификационный объект не найден
			error_message = "Неправильно введен код."
			return render(request, 'account/verification_failed.html', {'error': error_message,
																	   'form':form,
																	   'query':query,
																	   'pizza_results':pizza_results,
											   'market_results':market_results})

		if not verification.is_valid():
			# Верификационный код недействителен
			error_message = "Верификационный код недействителен или устарел."
			return render(request, 'account/verification_failed.html', {'error': error_message,
																		'form':form,
																	   'query':query,
																	   'pizza_results':pizza_results,
											   'market_results':market_results})

		if not verification.can_attempt():
			# Превышено количество попыток ввода кода
			error_message = "Превышено максимальное количество попыток ввода кода."
			return render(request, 'account/verification_failed.html', {'error': error_message,
																	   'form':form,
																	   'query':query,
																	   'pizza_results':pizza_results,
																	 'market_results':market_results})

		# Если все проверки пройдены успешно
		verification.increment_attempts()
		request.session['is_verified'] = True
		return redirect('account:profile_detail')

	# Если форма не валидна
	return render(request, 'account/verification.html', {'verify_form': verify_form,
														'form':form,
													   'query':query,
													   'pizza_results':pizza_results,
														'market_results':market_results})


@verification_required_for_profile
def profile_detail(request):
	
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

	phone_number = request.session.get('phone_number')
	if not Profile.objects.filter(phone_number=phone_number).exists():
		profile_form = ProfileEditForm(request.POST)
		if profile_form.is_valid():
			photo = profile_form.cleaned_data['photo']
			first_name = profile_form.cleaned_data['first_name']
			last_name = profile_form.cleaned_data['last_name']
			phone_number = request.session.get('phone_number')
			Profile.objects.create(phone_number=phone_number, first_name=first_name, last_name=last_name, photo=photo)
			request.session['is_profiled'] = True
			return redirect('account:profile_view')
		return render(request, 'account/profile_detail.html', {'profile_form':profile_form,
															  'form':form,
															   'query':query,
															   'pizza_results':pizza_results,
																'market_results':market_results})
	else:
		request.session['is_profiled'] = True
		return redirect('navigator:product_list')
	

@verification_required
def logout(request):
	# Удаляем данные, связанные с авторизацией пользователя
	if 'is_verified' in request.session:
		del request.session['is_verified']
	if 'phone_number' in request.session:
		del request.session['phone_number']
	if 'is_profiled' in request.session:
		del request.session['is_profiled']

	# Перенаправляем пользователя на главную страницу или на страницу входа
	return redirect('navigator:product_list')  # Измените 'main_page' на URL вашей главной страницы или страницы входа

@verification_required
def edit_profile(request):
	
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

	phone_number = request.session.get('phone_number')
	profile = get_object_or_404(Profile, phone_number=phone_number)

	if request.method == 'POST':
		profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
		if profile_form.is_valid():
			profile_form.save()
			# Вы можете перенаправить пользователя куда-то после успешного сохранения
			return redirect('account:profile_view')
	else:
		profile_form = ProfileEditForm(instance=profile)

	return render(request, 'account/edit_profile.html', {'profile_form': profile_form,
														'form':form,
													   'query':query,
													   'pizza_results':pizza_results,
														'market_results':market_results})

@verification_required
def profile_view(request):
	
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

	phone_number = request.session.get('phone_number')
	profile =  get_object_or_404(Profile, phone_number=phone_number)
	return render(request, 'account/profile_view.html', {'profile':profile,
														'form':form,
													   'query':query,
													   'pizza_results':pizza_results,
														'market_results':market_results})