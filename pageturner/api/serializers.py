from rest_framework import serializers
from reviews.models import Book
from members.models import Profile


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["user", "books_bookmarked", "books_read", "follows"]
