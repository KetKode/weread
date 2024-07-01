from enum import Enum

from api.serializers import BookSerializer, BookCollectionSerializer
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes


class SchemaTags(Enum):
    BOOK = "book"
    AUTHOR = "author"
    USER = "user"
    BOOK_COLLECTION = "book_collection"
    REC = "rec"


BOOK_API_METADATA = {
    "BookList": {"tags": [SchemaTags.BOOK.value], "summary": "Get all books from DB"},
    "BookCreate": {
        "tags": [SchemaTags.BOOK.value],
        "summary": "Create a new book",
        "parameters": [BookSerializer],
    },
    "BookGet": {"tags": [SchemaTags.BOOK.value], "summary": "Get a book by ID"},
    "BookUpdate": {"tags": [SchemaTags.BOOK.value], "summary": "Update a book by ID"},
    "BookDelete": {"tags": [SchemaTags.BOOK.value], "summary": "Delete a book by ID"},
    "BookmarkBook": {"tags": [SchemaTags.BOOK.value], "summary": "Bookmark a book"},
    "SearchFilters": {
        "tags": [SchemaTags.BOOK.value],
        "summary": "Search filters: title, author, ISBN, genres, age, book_collections, format, "
        "language, year range, year_from ,year_to",
        "parameters": [
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Title of the book. Case-insensitive.",
            ),
            OpenApiParameter(
                name="author",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Author of the book. Case-insensitive.",
            ),
            OpenApiParameter(
                name="isbn",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="ISBN of the book. Needs to be exact.",
            ),
            OpenApiParameter(
                name="genre",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Genre of the book. Selected from choices. Multiple values can be provided.",
            ),
            OpenApiParameter(
                name="age",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Age category of the book. Multiple values can be provided.",
            ),
            OpenApiParameter(
                name="book_collection",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Book collection names. Multiple values can be provided.",
            ),
            OpenApiParameter(
                name="format",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Format of the book. Multiple values can be provided.",
            ),
            OpenApiParameter(
                name="language",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Language of the book. Multiple values can be provided.",
            ),
            OpenApiParameter(
                name="year_from",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Start year for the book's publication date range.",
            ),
            OpenApiParameter(
                name="year_to",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="End year for the book's publication date range.",
            ),
        ],
    },
    "SearchBar": {
        "tags": [SchemaTags.BOOK.value],
        "summary": "Search bar: title, author, ISBN",
        "parameters": [
            OpenApiParameter(
                name="title",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Title of the book. Case-insensitive.",
            ),
            OpenApiParameter(
                name="author",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Author of the book. Case-insensitive.",
            ),
            OpenApiParameter(
                name="isbn",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="ISBN of the book. Needs to be exact.",
            ),
        ],
    },
}

RECS_API_METADATA = {
    "GeneralRecommendations": {
        "tags": [SchemaTags.REC.value],
        "summary": "Display recommendations for a not logged-in user",
    },
    "PersonalRecommendations": {
        "tags": [SchemaTags.REC.value],
        "summary": "Display recommendations for a logged-in user based on their likes",
    },
    "FriendsRecommendations": {
        "tags": [SchemaTags.REC.value],
        "summary": "Display recommendations based on user's friends' likes",
    },
    "LuckyBook": {"tags": [SchemaTags.REC.value], "summary": "Display a random book"},
}

BOOK_COLLECTION_API_METADATA = {
    "BookCollectionList": {
        "tags": [SchemaTags.BOOK_COLLECTION.value],
        "summary": "Get all book collections from DB",
    },
    "BookCollectionCreate": {
        "tags": [SchemaTags.BOOK_COLLECTION.value],
        "summary": "Create a new book collection",
        "parameters": [BookCollectionSerializer],
    },
    "BookCollectionGet": {
        "tags": [SchemaTags.BOOK_COLLECTION.value],
        "summary": "Get a book collection by ID",
    },
    "BookCollectionUpdate": {
        "tags": [SchemaTags.BOOK_COLLECTION.value],
        "summary": "Update a book collection by ID",
    },
    "BookCollectionDelete": {
        "tags": [SchemaTags.BOOK_COLLECTION.value],
        "summary": "Delete a book collection by ID",
    },
}
