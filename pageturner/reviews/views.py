from django.shortcuts import render, redirect, reverse
from .models import Book, Author, Review, SharedReview
from members.models import Snippet
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from members.forms import SnippetForm, CommentForm
from .forms import ReviewCommentForm
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
        rating = self.request.POST.get('rating')
        if rating:
            form.instance.rating = rating

        form.instance.user = self.request.user

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


@login_required
def review_like(request, pk):
    review = get_object_or_404(Review, id=pk)
    if review.likes.filter(id=request.user.id):
        review.likes.remove(request.user)
    else:
        review.likes.add(request.user)

    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def review_comment(request, pk):
    original_review = get_object_or_404(Review, id=pk)
    if request.method == "POST":
        form = ReviewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = original_review
            comment.user = request.user
            comment.save()
            messages.success(request, "Your comment has been successfully posted.")
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        form = CommentForm()
    return render(request, "reviews/comment_review.html", {"original_review": original_review, "form": form})


@login_required
def review_share(request, pk):
    review = get_object_or_404(Review, id=pk)

    shared_review = SharedReview.objects.create(original_review=review, user=request.user)

    return redirect('profile', pk=request.user.pk)


# def generate_random_dark_color():
#     r = random.randint(128, 255)  # Red component (128-255)
#     g = random.randint(0, 64)  # Green component (0-64, kept low for purple shades)
#     b = random.randint(128, 255)  # Blue component (128-255)
#     return "#{:02x}{:02x}{:02x}".format(r, g, b)


def genre_selection(request):
    unique_genres = Book.objects.exclude(tags=None).values_list('tags', flat=True).distinct()

    # Remove None values and split tags into individual genres
    genres_list = [genre.strip() for genres in unique_genres if genres for genre in genres.split(',')]

    # Remove duplicates by converting the list to a set and then back to a list
    unique_genres_list = list(set(genres_list))

    # Generate random colors for each genre
    # genre_color_mapping = {genre: generate_random_dark_color() for genre in unique_genres_list}
    #
    # # Create a list of tuples containing genre names and their corresponding colors
    # genre_color_tuples = [(genre, genre_color_mapping.get(genre, generate_random_dark_color())) for genre in
    #                       unique_genres_list]

    return render(request, "reviews/genres_list.html", {"unique_genres_list": unique_genres_list})