from . import views
from django.urls import path


urlpatterns = [
    path('', views.welcome_page, name="welcome_page"),
    path('book_search', views.book_search, name="book_search")
    ]