from django.urls import path

from . import views

urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register_user"),
    path('profile_list', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('update_user', views.update_user, name="update_user"),
    path('snippet_like/<int:pk>', views.snippet_like, name="snippet_like"),
    path('snippet_share/<int:pk>', views.snippet_share, name="snippet_share"),
    path('snippet_delete/<int:pk>', views.snippet_delete, name="snippet_delete"),
    path('snippet_edit/<int:pk>', views.snippet_edit, name="snippet_edit"),
    path('snippet_comment/<int:pk>', views.snippet_comment, name="snippet_comment"),
    path('comment_delete/<int:pk>', views.comment_delete, name="comment_delete"),
    path('comment_like/<int:pk>', views.comment_like, name="comment_like"),
    path('snippet/<int:snippet_id>/comment/<int:comment_id>/edit/', views.comment_edit, name="comment_edit"),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('follow/<int:pk>', views.follow, name="follow"),
    path('bookmark_book/<int:pk>', views.bookmark_book, name="bookmark_book"),
    path('mark_as_read/<int:pk>', views.mark_as_read, name="mark_as_read"),
    ]