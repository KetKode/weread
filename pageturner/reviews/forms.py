from django import forms

from .models import Review, BookImport, ReviewComment, AuthorImport


class BookSearchForm(forms.Form):
    search = forms.CharField(min_length=3, max_length=50, required=False, label="Search")


class BookImportForm(forms.ModelForm):
    class Meta:
        model = BookImport
        fields = ('csv_file',)


class AuthorImportForm(forms.ModelForm):
    class Meta:
        model = AuthorImport
        fields = ('csv_file',)


class ReviewForm(forms.ModelForm):
    content = forms.CharField(required=True,
                               widget=forms.widgets.Textarea(attrs={"placeholder": "Type your review here.",
                                                                     "class": "form-control center-content", }
                                                              ), label="", )
    rating = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Review
        exclude = ("date_created", "date_edited", "book", "written_by")


class ReviewCommentForm(forms.ModelForm):
    body = forms.CharField(required=True,
                            widget=forms.widgets.Textarea(attrs={"placeholder": "Type your comment here.",
                                                                  "class": "form-control", }
                                                           ), label="", )

    class Meta:
        model = ReviewComment
        fields = ["body"]

