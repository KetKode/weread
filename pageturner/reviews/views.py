from django.shortcuts import render, redirect, reverse
from .models import Book, Author
from django.db.models import Q
from .forms import BookSearchForm


def welcome_page(request):
    return render(request, "reviews/base.html")


