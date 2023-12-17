from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('v1/', include("dj_rest_auth.urls")),
    path('v1/registration/', include("dj_rest_auth.registration.urls")),
    path('books/', BookList.as_view(), name="books_api"),
    path('books/<int:pk>', BookDetail.as_view(), name="book_details_api"),
    path('recommendations/', recommended_books, name="recommended_books_api"),
    path('personal_recommendations', personal_recommendations, name="personal_recommendations_api"),
    path('friends_recommendations', friends_recommendations, name="friends_recommendations_api"),
    path('show_lucky_book', show_lucky_book, name="show_lucky_book_api"),
    path('like_book/<int:pk>', like_book, name="like_book_api"),
    path('book_collections', BookCollections.as_view(), name="book_collections_api"),
    path('book_collections/<int:pk>', show_book_collection, name="show_book_collection_api")
    ]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls'))
    ]