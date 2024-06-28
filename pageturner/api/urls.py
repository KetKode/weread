from django.urls import include, path

from api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"books", views.BookAPIViewSet)


urlpatterns = [
    # login, logout, registration
    path("v1/", include("dj_rest_auth.urls")),
    path("v1/registration/", include("dj_rest_auth.registration.urls")),
    path("", include(router.urls)),
    # # all books from the db
    # path('books/', BookList.as_view(), name="books_api"),
    # # one book on a page
    # path('books/<int:pk>/', BookDetail.as_view(), name="book_details_api"),
    # # recommendations carousel for not signed-in user
    # path('recommendations/', recommended_books, name="recommended_books_api"),
    # # recommendations carousel based on signed-in user's liked books (based on main genre)
    # path('personal_recommendations/', personal_recommendations, name="personal_recommendations_api"),
    # # recommendations carousel based on signed-in user's friends' liked/read/bookmarked books (based on main genre)
    # path('friends_recommendations/', friends_recommendations, name="friends_recommendations_api"),
    # # show a random book ("I'm feeling lucky")
    # path('show_lucky_book/', show_lucky_book, name="show_lucky_book_api"),
    # # bookmark a book (signed-in user)
    # path('bookmark_book/<int:pk>/', bookmark_book, name="bookmark_book_api"),
    # # show all available book collections
    # path('book_collections/', BookCollections.as_view(), name="book_collections_api"),
    # # show one book collection on a page
    # path('book_collections/<int:pk>/', show_book_collection, name="show_book_collection_api"),
    # # book search
    # path('book_search/', book_search, name="book_search"),
    # # email subscription
    # path('email_subscription/', email_subscription, name="email_subscription")
]

urlpatterns += [path("api-auth/", include("rest_framework.urls"))]
