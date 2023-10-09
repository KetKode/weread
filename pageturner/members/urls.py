from . import views
from django.urls import path


urlpatterns = [
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register_user"),
    path('profile_list', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name="profile"),
    path('update_user', views.update_user, name="update_user"),
    path('snippet_like/<int:pk>', views.snippet_like, name="snippet_like"),
    path('snippet_share/<int:pk>', views.snippet_share, name="snippet_share"),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('follow/<int:pk>', views.follow, name="follow"),
    ]