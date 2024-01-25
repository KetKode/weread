import random

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import Profile
from reviews.models import Book, BookCollection
from .serializers import BookSerializer, ProfileSerializer, BookCollectionSerializer


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
def recommended_books(request):
    """
    Display recommendations for a not logged-in user
    """

    books = list(Book.objects.all())
    recommended_books = random.sample(books, 10)
    book_serializer = BookSerializer(recommended_books, many=True)

    return Response(book_serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
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
            "profile_data": profile_serializer.data,
            "recommended_books": book_serializer.data
            }
        return Response(response_data)

    else:
        books = list(Book.objects.all())
        recommended_books = random.sample(books, 10)
        book_serializer = BookSerializer(recommended_books, many=True)

        response_data = {
            "profile_data": profile_serializer.data,
            "recommended_books": book_serializer.data
            }
        return Response(response_data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def friends_recommendations(request):
    """
    Display recommendations based on user's friends' likes
    """
    friends = Profile.objects.filter(followed_by=request.user.profile)
    friends_serializer = ProfileSerializer(friends, many=True)

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
            "friends": friends_serializer.data,
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


@api_view(['GET'])
def show_lucky_book(request):
    """
    Display a random book
    """
    books = list(Book.objects.all())
    lucky_book = random.choice(books)
    book_serializer = BookSerializer(lucky_book, many=False)
    return Response(book_serializer.data)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bookmark_book(request, pk):
    """
    Bookmark a book
    """
    book = get_object_or_404(Book, id=pk)
    book_serializer = BookSerializer(book)
    if book.bookmarks.filter(id=request.user.id):
        book.bookmarks.remove(request.user.profile)
    else:
        book.bookmarks.add(request.user.profile)
    return Response(book_serializer.data)


class BookCollections(APIView):
    """
    List all book collections
    """
    def get(self, request, *args, **kwargs):
        book_collections = BookCollection.objects.all()
        collection_serializer = BookCollectionSerializer(book_collections, many=True)

        return Response(collection_serializer.data)


@api_view(['GET'])
def show_book_collection(request, pk):
    """
    Display books in a book collection
    """
    book_collection = get_object_or_404(BookCollection, pk=pk)
    collection_serializer = BookCollectionSerializer(book_collection, many=False)

    return Response(collection_serializer.data)


@api_view(['GET', 'POST'])
def book_search(request):
    # queryset = Book.objects.all()
    # main_genres = Book.objects.values_list('main_genre', flat=True).distinct().order_by('main_genre')
    # main_age = Book.objects.exclude(main_age__isnull=True).exclude(main_age='').values_list
    # ('main_age', flat=True).distinct()
    # language = Book.objects.values_list('language', flat=True).distinct()
    # book_lists = BookCollection.objects.values_list('name', flat=True).distinct().order_by('name')
    # format_book = Book.objects.values_list('format_book', flat=True).distinct()
    # year = Book.objects.values_list('year', flat=True).distinct()

    # Get the search query and selected genres
    search_text = request.GET.get("search_text") or request.POST.get("search_text")
    selected_genres = request.GET.getlist("selected_genres")
    selected_age = request.GET.getlist("selected_age")
    selected_book_lists = request.GET.getlist("selected_book_lists")
    selected_format = request.GET.getlist("selected_format")
    selected_language = request.GET.getlist("selected_language")
    year_from = request.GET.get("year_from")
    year_to = request.GET.get("year_to")

    combined_filters = Q()

    if search_text:
        combined_filters &= (Q(title__icontains=search_text) | Q(author__name__icontains=search_text) |
                             Q(isbn__contains=search_text)
        )

    if selected_genres:
        combined_filters &= Q(main_genre__in=selected_genres)

    if selected_age:
        combined_filters &= Q(main_age__in=selected_age)

    if selected_book_lists:
        combined_filters &= Q(book_lists__name__in=selected_book_lists)

    if selected_format:
        combined_filters &= Q(format_book__in=selected_format)

    if selected_language:
        combined_filters &= Q(language__in=selected_language)

    if year_from and year_to:
        combined_filters &= Q(year__range=[year_from, year_to])

        # Apply the combined filters to the queryset
    books = Book.objects.filter(combined_filters)
    book_serializer = BookSerializer(books, many=True)

    return Response(book_serializer.data)


@api_view(['GET', 'POST'])
def email_subscription(request):

    subject = "Welcome to WeRead - Your Literary Adventure Begins!"

    message = """Dear ... ,

        Welcome to WeRead, the ultimate destination for book enthusiasts like yourself! We are thrilled to 
        have you join our community of avid readers who share a passion for the written word.

        At WeRead, we believe in the transformative power of books, and we're excited to embark on this 
        literary journey with you. Whether you're a seasoned bookworm or just starting to explore the world of 
        literature, WeRead is here to enhance your reading experience.

        Thank you for choosing WeRead as your literary companion. We look forward to being a part of your reading adventures!

        Happy reading!

        Best regards,
        The WeRead Team
        """
    recipients = [request.data, ]
    send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipients)

    return Response({'message': 'Email subscription successful'})


