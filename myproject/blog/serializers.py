from rest_framework import serializers
from .models import Post, Comment, Category, Reply, Profile
from django.contrib.auth.models import User
from .models import Subscriber

class ProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user_name', 'profile_picture', 'bio']

    def get_user_name(self, obj):
        return obj.user.username

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']# Add profile field to get profile details

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Include author details with profile
    category = CategorySerializer(read_only=True)
    comments = serializers.StringRelatedField(many=True, read_only=True)  # Display comments as strings

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'category', 'comments', 'image', 'description', 'slug']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.StringRelatedField(many=True, read_only=True)  # Display replies as strings

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'created_at', 'author', 'replies']

class ReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = ['id', 'comment', 'content', 'created_at', 'author']

class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email', 'date_subscribed']