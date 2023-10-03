from django.shortcuts import render, redirect, reverse
from .models import Book, Author
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def welcome_page(request):
    return render(request, "reviews/base.html")


def book_search(request):
    if request.method == "POST":
        searched = request.POST.get("searched")

        books = Book.objects.filter(Q(title__icontains=searched) | Q(author__name__icontains=searched))

        return render(request,
                  "reviews/search_results.html", {"searched": searched, "books": books})
    else:
        return render(request, "reviews/search_results.html", {})


class BookList(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = "book_list"


class BookDetail(DetailView):
    model = Book
    template_name = "reviews/book_detail.html"
    context_object_name = "book"


