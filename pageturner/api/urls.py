from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('books', BookList.as_view(), name="books"),
    path('books/<int:pk>', BookDetail.as_view(), name="book_details"),
    path('personal_recommendations', personal_recommendations, name="personal_recommendations"),
    path('friends_recommendations', friends_recommendations, name="friends_recommendations")
    ]

urlpatterns = format_suffix_patterns(urlpatterns)