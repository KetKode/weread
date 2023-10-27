from . import views
from django.urls import path
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', views.welcome_page, name="welcome_page"),
    path('book_search', views.book_search, name="book_search"),
    path('book_list', views.BookList.as_view(), name="book_list"),
    path('book_detail/<int:pk>', views.BookDetail.as_view(), name="book_detail"),
    path('book_detail/<int:pk>/review', views.ReviewCreateView.as_view(), name='create_review'),
    path('review_like/<int:pk>', views.review_like, name="review_like"),
    path('review_share/<int:pk>', views.review_share, name="review_share"),
    path('review_comment/<int:pk>', views.review_comment, name="review_comment"),

    ]