from api.serializers import BookSerializer

from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from enum import Enum


class SchemaTags(Enum):
    BOOK = "book"
    AUTHOR = "author"
    USER = "user"


BOOK_API_METADATA = {
    "BookList": {
        "tags": [SchemaTags.BOOK.value],
        "summary": "Get all books from DB"
        },
    "BookCreate": {
        "tags": [SchemaTags.BOOK.value],
        "summary": "Create a new book",
        "parameters": [BookSerializer]
        },
    "BookGet": {
        "tags": [SchemaTags.BOOK.value],
        "summary": "Get a book by ID"
        },
    "BookUpdate": {
        "tags": [SchemaTags.BOOK.value],
        "summary": "Update a book by ID"
        },
    "BookDelete": {
        "tags": [SchemaTags.BOOK.value],
        "summary": "Delete a book by ID"
        }
    }