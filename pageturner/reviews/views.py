from django.shortcuts import render, redirect, reverse
from .models import Book, Author
from django.db.models import Q
from .forms import BookSearchForm


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



