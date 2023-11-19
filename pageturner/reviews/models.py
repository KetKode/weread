from django.db import models
from django.contrib.auth.models import User
import PIL


class Publisher(models.Model):
    """A company that publishes books"""
    name = models.CharField(max_length=50, help_text="The name of the Publisher.")

    def __str__(self):
        return f"{self.name}"


class Author(models.Model):
    """A contributor to a Book, e.g. author, editor"""
    name = models.CharField(max_length=100, help_text="The name of the author", default=None)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    """A published book"""

    BEST_BOOK_OF_2023_CHOICES = [("No", "No"),
                                 ("Yes", "Yes")]

    title = models.CharField(max_length=200, help_text="The title of the book.")
    rating = models.FloatField(default=0, help_text="The rating of the book", null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    url = models.URLField(help_text="Link to the book page on Goodreads", default=None, null=True)
    cover_url = models.URLField(null=True, blank=True)
    summary = models.CharField(max_length=5000, help_text="Summary of the book", blank=True, null=True)
    main_genre = models.CharField(max_length=20, help_text="Main genre of the book", blank=True, null=True)
    genres = models.CharField(max_length=1000, help_text="Genres of the book (tags)", null=True, blank=True)
    number_of_pages = models.IntegerField(help_text="Number of pages in the book", blank=True, null=True)
    time = models.CharField(max_length=30, help_text="Time to finish the book", blank=True, null=True)
    amazon_link = models.URLField(help_text="Buy on Amazon", blank=True, null=True)
    audible_link = models.URLField(help_text="Buy on Audible", blank=True, null=True)
    year = models.IntegerField(help_text="Release year of the book", blank=True, null=True)
    format_book = models.CharField(max_length=50, help_text="Format of the book", blank=True, null=True)
    language = models.CharField(max_length=50, help_text="Language of the book", blank=True, null=True)
    isbn = models.CharField(max_length=15, help_text="ISBN", blank=True, null=True)
    isbn13 = models.CharField(max_length=15, help_text="ISBN13", blank=True, null=True)
    age = models.CharField(max_length=100, help_text="Age of book's audience", blank=True, null=True)
    main_age = models.CharField(max_length=20, help_text="Main age of the book", blank=True, null=True)
    best_books_of_2023 = models.CharField(max_length=3, choices=BEST_BOOK_OF_2023_CHOICES, default="No")

    def __str__(self):
        return f"{self.title} / {self.author} / {self.main_genre} / {self.best_books_of_2023} / {self.year}"

    def get_genres_list(self):
        return [genre.strip() for genre in self.genres.split(',')]

    def get_age_list(self):
        return [age_item.strip() for age_item in self.age.split(',')]


class BookCollection(models.Model):
    name = models.CharField(max_length=50, help_text="The name of the Book List")
    books = models.ManyToManyField(Book, related_name='book_lists', help_text="Books in the list")
    list_cover = models.ImageField(upload_to="media/", null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    written_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content = models.TextField(help_text="The Review text.")
    rating = models.CharField(help_text="The rating the reviewer has given.", max_length=10, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(null=True, help_text="The date and time this review was last edited.")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="The Book that this review is for.", related_name="reviews")
    likes = models.ManyToManyField(User, related_name="review_like", blank=True, default=0)

    def __str__(self):
        return f"Review for {self.book} / {self.rating}"

    def number_of_likes(self):
        return self.likes.count()


class SharedReview(models.Model):
    original_review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="shared_review")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shared by {self.user} at {self.shared_at}"


class ReviewComment(models.Model):
    user = models.ForeignKey(User, related_name="review_comment", on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="commented_review")
    likes = models.ManyToManyField(User, related_name="review_comment_like", blank=True)

    def __str__(self):
        return f"Review commented by {self.user} at {self.created_at} to {self.review}"

    def number_of_likes(self):
        return self.likes.count()


class BookImport(models.Model):
    csv_file = models.FileField(upload_to='uploads/')
    date_added = models.DateTimeField(auto_now_add=True)


