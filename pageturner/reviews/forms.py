from django import forms
from .models import Publisher, Review, Book
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class BookSearchForm(forms.Form):
    search_query = forms.CharField(min_length=3, max_length=50, required=False, label="Search")
