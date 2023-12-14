from rest_framework import serializers, permissions
from reviews.models import Book, BookCollection
from members.models import Profile


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCollection
        fields = ["name", "list_cover"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "books_bookmarked", "books_read", "books_liked", "follows"]
