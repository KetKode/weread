from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .serializers import BookSerializer, ProfileSerializer
from reviews.models import Book
from members.models import Profile
from django.db.models import Q
import random


class BookList(APIView):
    """
    List all books from the db
    """
    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetail(APIView):
    """
    Display a page dedicated to one book
    """
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def personal_recommendations(request):
    """
    Display personal recommendations based on user's likes
    """

    profile_serializer = ProfileSerializer(request.user.profile)

    liked_books = Book.objects.filter(Q(liked_books=True) & Q(main_genre__isnull=False))

    if liked_books:
        main_liked_genres = [book.main_genre for book in liked_books]
        recommended_books = Book.objects.filter(Q(main_genre__in=main_liked_genres)).order_by('?')[:10]
        book_serializer = BookSerializer(recommended_books, many=True)

        response_data = {
            "recommended_books": book_serializer.data,
            "profile_serializer": profile_serializer.data
            }
        return Response(response_data)

    else:
        books = list(Book.objects.all())
        recommended_books = random.sample(books, 10)
        book_serializer = BookSerializer(recommended_books, many=True)

        response_data = {
            "recommended_books": book_serializer.data,
            "profile_serializer": profile_serializer.data
            }
        return Response(response_data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def friends_recommendations(request):
    """
    Display recommendations based on user's friends' likes
    """
    friends = Profile.objects.filter(followed_by=request.user.profile)

    if friends:
        random_friend = random.choice(friends)
        random_friends_books = Book.objects.filter(Q(liked_books=random_friend)
                                                   | Q(bookmarks=random_friend)
                                                   | Q(read_books=random_friend))

        main_random_friends_liked_genres = [book.main_genre for book in random_friends_books]
        random_friends_recommended_books = Book.objects.filter(main_genre__in=main_random_friends_liked_genres).order_by('?')
        random_friends_recommendations = random_friends_recommended_books[:10]
        book_serializer = BookSerializer(random_friends_recommendations, many=True)
        response_data = {
            "recommended_books": book_serializer.data,
                }
        return Response(response_data)
    else:
        books = list(Book.objects.all())
        recommended_books = random.sample(books, 10)
        book_serializer = BookSerializer(recommended_books, many=True)

        response_data = {
            "recommended_books": book_serializer.data
            }

        return Response(response_data)


