from django import forms
from .models import Profile
from django.core.validators import RegexValidator
	
class PhoneNumberForm(forms.Form):
	phone_regex = RegexValidator(regex=r'^\+?1?\d{7,15}$')
	phone_number = forms.CharField(label='Номер телефона', validators=[phone_regex], max_length=17)

class VerificationCodeForm(forms.Form):
    code = forms.CharField(label='Код подтверждения', max_length=6)

	
class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('photo', 'first_name', 'last_name')
	
class EditProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('photo', 'first_name', 'last_name', 'email')