from django import forms
from .models import Publisher, Review, Book, BookImport
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class BookSearchForm(forms.Form):
    search = forms.CharField(min_length=3, max_length=50, required=False, label="Search")


class BookImportForm(forms.ModelForm):
    class Meta:
        model = BookImport
        fields = ('csv_file',)


class ReviewForm(forms.ModelForm):
    content = forms.CharField(required=True,
                            widget=forms.widgets.Textarea(attrs={"placeholder": "Type your review here.",
                                                                  "class": "form-control center-content", }
                                                           ), label="", )

    RATING_CHOICES = [
        ('1', '⭐'),
        ('2', '⭐⭐'),
        ('3', '⭐⭐⭐'),
        ('4', '⭐⭐⭐⭐'),
        ('5', '⭐⭐⭐⭐⭐')
        ]

    rating = forms.MultipleChoiceField(required=True, choices=RATING_CHOICES, )


    class Meta:
        model = Review
        exclude = ("date_created", "date_edited", "book", "written_by")

