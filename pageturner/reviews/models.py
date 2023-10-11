from django.db import models
from django.contrib.auth.models import AbstractUser


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
    title = models.CharField(max_length=70, help_text="The title of the book.")
    rating_small = models.CharField(default=0, max_length=50, help_text="The smaller rating of the book", null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    url = models.URLField(help_text="Link to the book page on Goodreads", default=None, null=True)
    cover_url = models.URLField(null=True, blank=True)
    summary = models.CharField(max_length=2000, help_text="Summary of the book", blank=True, null=True)
    genres = models.CharField(max_length=1000, help_text="Genres of the book", null=True, blank=True)

    def __str__(self):
        return f"{self.title} / {self.author}"


class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True, help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(null=True, help_text="The date and time this review was last edited.")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="The Book that this review is for.")

    def __str__(self):
        return f"Review for {self.book} / {self.rating}"


class BookImport(models.Model):
    csv_file = models.FileField(upload_to='uploads/')
    date_added = models.DateTimeField(auto_now_add=True)


