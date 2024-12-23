from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('profile/', views.UserProfileListView.as_view(), name='profile'),
    path('profile/<str:username>/', views.profile_view, name='profile_detail'),
    path('create_post/', views.PostCreate.as_view(), name='create_post'),
    path('like/<int:post_id>/', views.post_like, name='post_like'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('profile/<str:username>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/delete/', views.delete_profile, name='delete_profile'),
]

