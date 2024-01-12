from rest_framework import serializers, permissions
from reviews.models import Book, BookCollection, Author
from members.models import Profile


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Book
        fields = "__all__"


class BookCollectionSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = BookCollection
        fields = ["id", "name", "books"]


class ProfileSerializer(serializers.ModelSerializer):
    books_bookmarked = BookSerializer(many=True, read_only=True)
    books_read = BookSerializer(many=True, read_only=True)
    books_liked = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "books_bookmarked", "books_read", "books_liked"]
