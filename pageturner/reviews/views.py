from django.shortcuts import render, redirect, reverse
from .models import Book, Author
from members.models import Snippet
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from members.forms import SnippetForm
from django.contrib import messages


def welcome_page(request):
    if request.user.is_authenticated:
        form = SnippetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                snippet = form.save(commit=False)
                snippet.user = request.user
                snippet.save()
                messages.success(request, "Your snippet has been posted!")
                return redirect("welcome_page")

        snippets = Snippet.objects.all().order_by("-created_at")
        return render(request, "reviews/base.html", {"snippets": snippets, "form": form})
    else:
        snippets = Snippet.objects.all().order_by("-created_at")
        return render(request, "reviews/base.html", {"snippets": snippets})



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
    template_name = 'reviews/book_list.html'
    context_object_name = "book_list"
    paginate_by = 10

    def get_queryset(self):
        return Book.objects.order_by('pk')


class BookDetail(DetailView):
    model = Book
    template_name = "reviews/book_detail.html"
    context_object_name = "book"



