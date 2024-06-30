from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register(r"books", views.BookAPIViewSet)
router.register(r"book_collection", views.BookCollectionViewSet)

urlpatterns = [
    path("v1/", include("dj_rest_auth.urls")),
    path("v1/registration/", include("dj_rest_auth.registration.urls")),
    path("", include(router.urls)),
    path('recommendations/', views.recommended_books, name="recommended_books"),
    path('personal_recommendations/', views.personal_recommendations, name="personal_recommendations"),
    path('friends_recommendations/', views.friends_recommendations, name="friends_recommendations"),
    path('show_lucky_book/', views.show_lucky_book, name="show_lucky_book"),
    path('bookmark_book/<int:pk>/', views.bookmark_book, name="bookmark_book"),
    # path('book_search/', book_search, name="book_search"),
    # # email subscription
    # path('email_subscription/', email_subscription, name="email_subscription")
]

urlpatterns += [path("api-auth/", include("rest_framework.urls"))]
