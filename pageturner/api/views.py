import random

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView

from api.schema_data import BOOK_API_METADATA, BOOK_COLLECTION_API_METADATA
from members.models import Profile
from reviews.models import Book, BookCollection
from .serializers import (
    BookSerializer,
    ProfileSerializer,
    BookCollectionSerializer,
)


class BookAPIViewSet(ModelViewSet):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer

    fiter_backends = [DjangoFilterBackend]

    @extend_schema(**BOOK_API_METADATA["BookList"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(**BOOK_API_METADATA["BookCreate"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(**BOOK_API_METADATA["BookGet"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(**BOOK_API_METADATA["BookUpdate"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(**BOOK_API_METADATA["BookUpdate"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(**BOOK_API_METADATA["BookDelete"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@api_view()
@extend_schema(**BOOK_API_METADATA["GeneralRecommendations"])
def recommended_books(request):

    books = list(Book.objects.all())
    recommendations = random.sample(books, 10)
    book_serializer = BookSerializer(recommendations, many=True)

    return Response(book_serializer.data)


@api_view()
@extend_schema(**BOOK_API_METADATA["PersonalRecommendations"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def personal_recommendations(request):
    profile_serializer = ProfileSerializer(request.user.profile)

    liked_books = Book.objects.filter(Q(liked_books=True) & Q(main_genre__isnull=False))

    if liked_books:
        main_liked_genres = [book.main_genre for book in liked_books]
        recommendations = Book.objects.filter(
            Q(main_genre__in=main_liked_genres)
        ).order_by("?")[:10]
        book_serializer = BookSerializer(recommendations, many=True)

        response_data = {
            "profile_data": profile_serializer.data,
            "recommended_books": book_serializer.data,
        }
        return Response(response_data)

    else:
        books = list(Book.objects.all())
        recommendations = random.sample(books, 10)
        book_serializer = BookSerializer(recommendations, many=True)

        response_data = {
            "profile_data": profile_serializer.data,
            "recommended_books": book_serializer.data,
        }
        return Response(response_data)


@api_view()
@extend_schema(**BOOK_API_METADATA["FriendsRecommendations"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def friends_recommendations(request):
    friends = Profile.objects.filter(followed_by=request.user.profile)
    friends_serializer = ProfileSerializer(friends, many=True)

    if friends:
        random_friend = random.choice(friends)
        random_friends_books = Book.objects.filter(
            Q(liked_books=random_friend)
            | Q(bookmarks=random_friend)
            | Q(read_books=random_friend)
        )

        main_random_friends_liked_genres = [
            book.main_genre for book in random_friends_books
        ]
        random_friends_recommended_books = Book.objects.filter(
            main_genre__in=main_random_friends_liked_genres
        ).order_by("?")
        random_friends_recommendations = random_friends_recommended_books[:10]
        book_serializer = BookSerializer(random_friends_recommendations, many=True)

        response_data = {
            "friends": friends_serializer.data,
            "recommended_books": book_serializer.data,
        }
        return Response(response_data)
    else:
        books = list(Book.objects.all())
        recommendations = random.sample(books, 10)
        book_serializer = BookSerializer(recommendations, many=True)

        response_data = {"recommended_books": book_serializer.data}

        return Response(response_data)


@api_view()
@extend_schema(**BOOK_API_METADATA["LuckyBook"])
def show_lucky_book(request):
    books = list(Book.objects.all())
    lucky_book = random.choice(books)
    serializer_class = BookSerializer(lucky_book, many=False)
    return Response(serializer_class.data)


@api_view()
@extend_schema(**BOOK_API_METADATA["BookmarkBook"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bookmark_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    serializer_class = BookSerializer(book)
    if book.bookmarks.filter(id=request.user.id):
        book.bookmarks.remove(request.user.profile)
    else:
        book.bookmarks.add(request.user.profile)
    return Response(serializer_class.data)


class BookCollectionViewSet(ModelViewSet):
    queryset = BookCollection.objects.select_related("books").all()
    serializer_class = BookCollectionSerializer

    filter_backends = [DjangoFilterBackend]

    @extend_schema(**BOOK_COLLECTION_API_METADATA["BookCollectionList"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(**BOOK_COLLECTION_API_METADATA["BookCollectionCreate"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(**BOOK_COLLECTION_API_METADATA["BookCollectionGet"])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(**BOOK_COLLECTION_API_METADATA["BookCollectionUpdate"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(**BOOK_COLLECTION_API_METADATA["BookCollectionUpdate"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(**BOOK_COLLECTION_API_METADATA["BookCollectionDelete"])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(**BOOK_API_METADATA["SearchBar"])
class SearchBarApiListView(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()

        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        isbn = self.request.query_params.get("isbn")

        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if author is not None:
            queryset = queryset.filter(author__name__icontains=author)
        if isbn is not None:
            queryset = queryset.filter(isbn=isbn)

        return queryset


@extend_schema(**BOOK_API_METADATA["SearchFilters"])
class SearchFiltersApiListView(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all()

        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        isbn = self.request.query_params.get("isbn")

        selected_genres = self.request.query_params.getlist("genre")
        selected_age = self.request.query_params.getlist("age")
        selected_book_collections = self.request.query_params.getlist("book_collection")
        selected_format = self.request.query_params.getlist("format")
        selected_language = self.request.query_params.getlist("language")
        year_from = self.request.query_params.get("year_from")
        year_to = self.request.query_params.get("year_to")

        combined_filters = Q()

        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if author is not None:
            queryset = queryset.filter(author__name__icontains=author)
        if isbn is not None:
            queryset = queryset.filter(isbn=isbn)

        if selected_genres:
            combined_filters &= Q(main_genre__in=selected_genres)

        if selected_age:
            combined_filters &= Q(main_age__in=selected_age)

        if selected_book_collections:
            combined_filters &= Q(book_lists__name__in=selected_book_collections)

        if selected_format:
            combined_filters &= Q(format_book__in=selected_format)

        if selected_language:
            combined_filters &= Q(language__in=selected_language)

        if year_from and year_to:
            combined_filters &= Q(year__range=[year_from, year_to])
        elif year_from:
            combined_filters &= Q(year__gte=year_from)
        elif year_to:
            combined_filters &= Q(year__lte=year_to)

        return queryset.filter(combined_filters)


# @api_view(['GET', 'POST'])
# def email_subscription(request):
#
#     if request.method == "POST":
#         serializer = EmailSubscriptionSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             try:
#                 user, created = EmailSubscription.objects.get_or_create(email=email)
#                 if not created:
#                     return Response({'error': 'Email already subscribed'}, status=400)
#             except IntegrityError:
#                 return Response({'error': 'Error creating subscription'}, status=500)
#
#             subject = "Welcome to WeRead - Your Literary Adventure Begins!"
#
#             message = """Dear ... ,
#
#                 Welcome to WeRead, the ultimate destination for book enthusiasts like yourself! We are thrilled to
#                 have you join our community of avid readers who share a passion for the written word.
#
#                 At WeRead, we believe in the transformative power of books, and we're excited to embark on this
#                 literary journey with you. Whether you're a seasoned bookworm or just starting to explore the world of
#                 literature, WeRead is here to enhance your reading experience.
#
#                 Thank you for choosing WeRead as your literary companion. We look forward to being a part of your reading adventures!
#
#                 Happy reading!
#
#                 Best regards,
#                 The WeRead Team
#                 """
#
#             recipients = [email, ]
#
#             send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=recipients)
#
#             return Response({'message': 'Email subscription successful'})
#         else:
#             return Response({'error': 'Invalid data provided'}, status=400)
#
#     elif request.method == 'GET':
#         # Handle GET request if needed
#         return Response({'message': 'GET request received'})
