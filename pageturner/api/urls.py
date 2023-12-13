from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *


urlpatterns = [
    path('books/', BookList.as_view())
    ]

urlpatterns = format_suffix_patterns(urlpatterns)