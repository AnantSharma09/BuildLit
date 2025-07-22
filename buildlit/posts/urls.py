from django.urls import path
from .views import PostListView, PostDetailView, MediaListView, LikeListView, CommentListView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('media/', MediaListView.as_view(), name='media-list'),
    path('likes/', LikeListView.as_view(), name='like-list'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
]
