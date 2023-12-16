from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('books', BookList.as_view(), name="books"),
    path('books/<int:pk>', BookDetail.as_view(), name="book_details"),
    path('recommendations', recommended_books, name="recommended_books"),
    path('personal_recommendations', personal_recommendations, name="personal_recommendations"),
    path('friends_recommendations', friends_recommendations, name="friends_recommendations"),
    path('show_lucky_book', show_lucky_book, name="show_lucky_book"),
    path('like_book/<int:pk>', like_book, name="like_book"),
    path('book_collections', BookCollections.as_view(), name="book_collections"),
    path('book_collections/<int:pk>', show_book_collection, name="show_book_collection")
    ]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls'))
    ]