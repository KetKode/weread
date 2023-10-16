from django import forms
from .models import Snippet, Profile, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import UpdateView


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm (UserCreationForm):
    email = forms.EmailField (
        label="",
        widget=forms.EmailInput (attrs={'class': 'form-control', 'placeholder': 'Email Address'})
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__ (*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''


class ProfilePicForm (forms.ModelForm):
    profile_image = forms.ImageField(label="", widget=forms.FileInput(attrs={'class': 'form-control'}))
    profile_bio = forms.CharField(label="Profile Bio", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Profile Bio'}))
    homepage_link = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Website Link'}))
    facebook_link = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Facebook Link'}))
    instagram_link = forms.CharField(label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Instagram Link'}))

    class Meta:
        model = Profile
        fields = ('profile_image', 'profile_bio', 'homepage_link', 'instagram_link', 'facebook_link')


class SnippetForm(forms.ModelForm):
    body = forms.CharField(required=True,
                            widget=forms.widgets.Textarea(attrs={"placeholder": "Type your snippet here.",
                                                                  "class": "form-control", }
                                                           ), label="", )
    class Meta:
        model = Snippet
        exclude = ("user", "likes")


class CommentForm(forms.ModelForm):
    body = forms.CharField(required=True,
                            widget=forms.widgets.Textarea(attrs={"placeholder": "Type your comment here.",
                                                                  "class": "form-control", }
                                                           ), label="", )

    class Meta:
        model = Comment
        fields = ["body"]


class SnippetUpdate(forms.ModelForm):
    body = forms.CharField(required=True,
                            widget=forms.widgets.Textarea(attrs={"placeholder": "Type your snippet here.",
                                                                  "class": "form-control", }
                                                           ), label="", )

    class Meta:
        model = Snippet
        fields = ["body"]


class CommentUpdate(forms.ModelForm):
    body = forms.CharField(required=True,
                            widget=forms.widgets.Textarea(attrs={"placeholder": "Type your comment here.",
                                                                  "class": "form-control", }
                                                           ), label="", )

    class Meta:
        model = Comment
        fields = ["body"]
