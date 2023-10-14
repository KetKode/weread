from django.shortcuts import render, redirect, reverse
from .models import Book, Author, Review
from members.models import Snippet
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from members.forms import SnippetForm
from django.contrib import messages
from .forms import ReviewForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
import random


def welcome_page(request):

    books = list(Book.objects.all())
    random_books = random.sample(books, 12)

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
        return render(request, "reviews/base.html", {"snippets": snippets, "form": form, "random_books": random_books})
    else:
        snippets = Snippet.objects.all().order_by("-created_at")
        return render(request, "reviews/base.html", {"snippets": snippets, "random_books": random_books})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, id=book_id)
        context['book'] = book

        context['reviews'] = book.reviews.all()
        return context


class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/create_review.html"

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.rating = form.cleaned_data['rating']

        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, id=book_id)
        form.instance.book = book

        form.instance.written_by = self.request.user

        messages.success(self.request, "The review was created successfully.")
        return super(ReviewCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book_id = self.kwargs.get('pk')
        book = get_object_or_404(Book, id=book_id)
        context['book'] = book
        return context
