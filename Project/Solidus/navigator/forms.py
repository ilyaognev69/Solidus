from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'search-input', 'type':'text', 'style':'flex-grow: 1; padding: 7px; margin-right: 10px; border: 1px solid #ddd; border-radius: 4px;'})
    )