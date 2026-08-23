from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed_view, name='social_feed'),
    path('like/<int:post_id>/', views.like_post, name='social_like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='social_add_comment'),
    path('profile/<str:username>/', views.profile_view, name='social_profile'),
    path('follow/<str:username>/', views.follow_user, name='social_follow_user'),
    path('register/', views.social_register, name='social_register'),
    path('login/', views.social_login, name='social_login'),
    path('logout/', views.social_logout, name='social_logout'),
]