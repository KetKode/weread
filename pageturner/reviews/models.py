from django.db import models
from django.contrib.auth.models import User


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
    title = models.CharField(max_length=200, help_text="The title of the book.")
    rating = models.CharField(default=0, max_length=50, help_text="The smaller rating of the book", null=True, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    url = models.URLField(help_text="Link to the book page on Goodreads", default=None, null=True)
    cover_url = models.URLField(null=True, blank=True)
    summary = models.CharField(max_length=5000, help_text="Summary of the book", blank=True, null=True)
    tags = models.CharField(max_length=1000, help_text="Genres of the book (tags)", null=True, blank=True)
    number_of_pages = models.IntegerField(help_text="Number of pages in the book.", blank=True, null=True)
    time = models.CharField(max_length=30, help_text="Time to finish the book.", blank=True, null=True)
    amazon_link = models.URLField(help_text="Buy on Amazon.", blank=True, null=True)
    audible_link = models.URLField(help_text="Buy on Amazon.", blank=True, null=True)

    def __str__(self):
        return f"{self.title} / {self.author}"

    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',')]


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


