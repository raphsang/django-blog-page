from datetime import timedelta
from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password  # Make sure this is imported
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from django.db.models import Count
from .models import Post, Comment, Reply, Category
from .serializers import PostSerializer, CommentSerializer, CategorySerializer, ReplySerializer, UserSerializer
from django.core.exceptions import PermissionDenied
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Profile
from .serializers import ProfileSerializer
from .models import Subscriber
from .serializers import SubscriberSerializer
from rest_framework.views import APIView

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]  # Allow all users to view profiles

    def get_queryset(self):
        # Allow all profiles to be accessed
        return Profile.objects.all()

    def perform_update(self, serializer):
        user = self.request.user
        profile = self.get_object()
        # Restrict editing to the profile owner only
        if profile.user != user:
            raise PermissionDenied("You do not have permission to edit this profile.")
        serializer.save()
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile = super().get_object()
        if profile.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to access this profile.")
        return profile
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category']
    ordering_fields = ['created_at']
    search_fields = ['title']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            print(f"Search term received: {search_term}")
        return queryset

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user)
        else:
            raise PermissionDenied("You must be logged in to create a post.")

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        if post_id:
            return Comment.objects.filter(post_id=post_id)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all().order_by('-created_at')
    serializer_class = ReplySerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        comment_id = self.request.query_params.get('comment')
        if comment_id:
            return Reply.objects.filter(comment_id=comment_id)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return Response({'error': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
            user = User.objects.create_user(username=username, email=email, password=password)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        except IntegrityError:
            return Response({'error': 'Username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
class TrendingTopicsView(generics.GenericAPIView):
    
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        recent_date = timezone.now() - timedelta(days=30)
        trending_posts = Post.objects.filter(created_at__gte=recent_date, trending=True)
        serializer = PostSerializer(trending_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TrendingPostsView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        recent_date = timezone.now() - timedelta(days=30)
        trending_posts = Post.objects.filter(created_at__gte=recent_date, trending=True)
        serializer = PostSerializer(trending_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Here we are assuming that client will handle token removal
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    
class SubscribeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print('Received POST request')
        serializer = SubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print('Subscription successful')
            return Response({'message': 'Subscription successful!'}, status=status.HTTP_201_CREATED)
        print('Serializer errors:', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

