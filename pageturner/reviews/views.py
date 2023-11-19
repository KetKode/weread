from django.shortcuts import render, redirect, reverse
from .models import Book, Author, Review, SharedReview, BookCollection
from members.models import Snippet
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from members.forms import SnippetForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ReviewCommentForm
from django.contrib import messages
from .forms import ReviewForm
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
import random
from .filters import BookFilter


def welcome_page(request):

    books = list(Book.objects.all())
    random_books = random.sample(books, 12)
    book_collections = list(BookCollection.objects.all())

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
        return render(request, "reviews/base.html", {"snippets": snippets, "form": form, "random_books": random_books,
                                                     "book_collections": book_collections})
    else:
        snippets = Snippet.objects.all().order_by("-created_at")
        return render(request, "reviews/base.html", {"snippets": snippets, "random_books": random_books,
                                                     "book_collections": book_collections})


def book_search(request):
    queryset = Book.objects.all()
    main_genres = Book.objects.values_list('main_genre', flat=True).distinct().order_by('main_genre')
    main_age = Book.objects.exclude(main_age__isnull=True).exclude(main_age='').values_list('main_age', flat=True).distinct()
    language = Book.objects.values_list('language', flat=True).distinct()
    book_lists = BookCollection.objects.values_list('name', flat=True).distinct().order_by('name')
    format_book = Book.objects.values_list('format_book', flat=True).distinct()

    # Get the search query and selected genres
    searched = request.GET.get("searched") or request.POST.get("searched")
    selected_genres = request.GET.getlist("selected_genres")
    selected_age = request.GET.getlist("selected_age")
    selected_book_lists = request.GET.getlist("selected_book_lists")
    selected_format = request.GET.getlist("selected_format")
    selected_language = request.GET.getlist("selected_language")

    # Apply filters based on search and selected genres
    if searched and selected_genres:
        books = Book.objects.filter(Q(title__icontains=searched) & Q(author__name__icontains=searched) & Q(main_genre__in=selected_genres))
    elif searched:
        books = Book.objects.filter(Q(title__icontains=searched) | Q(author__name__icontains=searched))
    elif selected_genres:
        books = Book.objects.filter(main_genre__in=selected_genres)
    elif selected_age:
        books = Book.objects.filter(main_age__in=selected_age)
    elif selected_book_lists:
        books = Book.objects.filter(book_lists__name__in=selected_book_lists)
    elif selected_format:
        books = Book.objects.filter(format_book__in=selected_format)
    elif selected_language:
        books = Book.objects.filter(language__in=selected_language)
    else:
        books = Book.objects.all()

    return render(
        request,
        "reviews/search_results.html",
        {"searched": searched,
         "books": books,
         "main_genres": main_genres,
         "selected_genres": selected_genres,
         "main_age": main_age,
         "selected_age": selected_age,
         "language": language,
         "selected_language": selected_language,
         "format_book": format_book,
         "selected_format": selected_format,
         "book_lists": book_lists,
         "selected_book_lists": selected_book_lists},
        )


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


def show_book_collections(request, pk):
    book_collection = get_object_or_404(BookCollection, pk=pk)

    books = book_collection.books.all()

    items_per_page = 10
    paginator = Paginator(books, items_per_page)
    page_number = request.GET.get('page')
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page.
        page = paginator.page(paginator.num_pages)

    return render(request, "reviews/book_collections.html", {"book_collection": book_collection, "books": page})


def book_genres_list(request, genre):

    books_with_genre = Book.objects.filter(genres__icontains=genre)

    items_per_page = 10
    paginator = Paginator(books_with_genre, items_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, "reviews/book_genres_list.html", {'books': page, 'genre': genre})


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
    unique_genres = Book.objects.exclude(tags=None).values_list('genres', flat=True).distinct()

    # Remove None values and split tags into individual genres
    genres_list = [genre.strip() for genres in unique_genres if genres for genre in genres.split(',')]

    # Remove duplicates by converting the list to a set and then back to a list
    unique_genres_list = list(set(genres_list))

    return render(request, "reviews/genres_list.html", {"unique_genres_list": unique_genres_list})



