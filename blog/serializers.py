from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost, Comment, Like

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    display_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'guest_name', 'display_name', 'created_at', 'is_approved']
        read_only_fields = ['author', 'created_at', 'is_approved']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']

class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'content', 'author', 'timestamp', 
            'updated_at', 'status', 'slug', 'excerpt', 
            'comments', 'likes', 'like_count', 'comment_count'
        ]
        read_only_fields = ['author', 'timestamp', 'updated_at', 'slug', 'like_count', 'comment_count']

class BlogPostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_count = serializers.ReadOnlyField()
    comment_count = serializers.ReadOnlyField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'excerpt', 'author', 'timestamp', 
            'status', 'slug', 'like_count', 'comment_count'
        ]
        read_only_fields = ['author', 'timestamp', 'slug', 'like_count', 'comment_count']

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'guest_name'] 