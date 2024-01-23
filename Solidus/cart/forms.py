from django import forms

class CartAddProductForm(forms.Form):
	quantity = forms.IntegerField(min_value=1, max_value=99, initial=1, label="")
	override = forms.BooleanField(required=False,
								 initial=False,
								 widget=forms.HiddenInput)
	def clean_quantity(self):
		"""Дополнительная проверка количества перед добавлением в корзину."""
		quantity = self.cleaned_data['quantity']
		if quantity > 99:
			raise forms.ValidationError("Вы не можете добавить больше 99 товаров.")
		return quantity
