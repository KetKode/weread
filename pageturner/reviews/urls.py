from . import views
from django.urls import path

urlpatterns = [
    path('home/', views.welcome_page, name="welcome_page")
    ]