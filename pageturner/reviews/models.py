from django.db import models


class Publisher(models.Model):
    """A company that publishes books"""
    name = models.CharField(max_length=50, help_text="The name of the Publisher.")

    def __str__(self):
        return f"{self.name} / {self.website}"


class Author(models.Model):
    """A contributor to a Book, e.g. author, editor"""
    first_name = models.CharField(max_length=50, help_text="The author's first name or names.")
    last_name = models.CharField(max_length=50, help_text="The author's last name or names.")

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Book(models.Model):
    """A published book"""
    title = models.CharField(max_length=70, help_text="The title of the book.")
    publication_date = models.DateField(verbose_name="Date the book was published.")
    isbn = models.CharField(max_length=20, verbose_name="ISBN number of the book.")
    summary = models.TextField(default=None)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=None)
    cover = models.ImageField(upload_to="book_covers/", null=True, blank=True)
    sample = models.FileField(upload_to="book_samples/", null=True, blank=True)

    def __str__(self):
        return f"{self.title} / {self.isbn} / {self.author}"


class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True, help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(null=True, help_text="The date and time this review was last edited.")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="The Book that this review is for.")

    def __str__(self):
        return f"Review for {self.book} / {self.rating}"
