from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, ProfileViewSet, ProfileDetailView, CommentViewSet, ReplyViewSet, CategoryViewSet, RegisterView,
    TrendingTopicsView, TrendingPostsView, CommentDetailView, 
    PostDetailView, LoginView, LogoutView, SubscribeView
)

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'replies', ReplyViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('trending-topics/', TrendingTopicsView.as_view(), name='trending-topics'),
    path('trending-posts/', TrendingPostsView.as_view(), name='trending-posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
] + router.urls
