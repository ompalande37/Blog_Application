from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import BlogPost, Comment, Like
from .serializers import (
    BlogPostSerializer, BlogPostListSerializer, 
    CommentSerializer, CreateCommentSerializer, LikeSerializer, UserSerializer
)
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.contrib import messages

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['timestamp', 'title']
    ordering = ['-timestamp']

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostSerializer

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        if self.action == 'list':
            # Only show published posts in list view
            queryset = queryset.filter(status='published')
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # Only allow authors to update their own posts
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You can only edit your own posts.")
        serializer.save()

    def perform_destroy(self, instance):
        # Only allow authors to delete their own posts
        if instance.author != self.request.user:
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        like, created = Like.objects.get_or_create(post=post, user=user)
        
        if not created:
            # If like already exists, remove it (toggle)
            like.delete()
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Post liked'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.filter(is_approved=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def add_comment(self, request, pk=None):
        post = self.get_object()
        serializer = CreateCommentSerializer(data=request.data)
        
        if serializer.is_valid():
            # Handle anonymous comments
            if request.user.is_authenticated:
                comment = serializer.save(post=post, author=request.user)
            else:
                guest_name = request.data.get('guest_name', 'Anonymous')
                comment = serializer.save(post=post, author=None, guest_name=guest_name)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(is_approved=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own comments.")
        instance.delete()

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise permissions.PermissionDenied("You can only remove your own likes.")
        instance.delete()


# Frontend Views
class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        # Show all published posts to everyone
        return BlogPost.objects.filter(status='published').order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_create_button'] = self.request.user.is_authenticated
        context['show_logout_button'] = self.request.user.is_authenticated
        return context

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    
    def get_queryset(self):
        # Show published posts to everyone
        return BlogPost.objects.filter(status='published')
    
    # Remove the dispatch login check so anyone can view published posts
    # def dispatch(self, request, *args, **kwargs):
    #     if not request.user.is_authenticated:
    #         messages.warning(request, 'Please login to view blog posts.')
    #         return redirect('user_login')
    #     return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        comment_content = request.POST.get('comment_content')
        if not comment_content:
            messages.error(request, 'Please enter a comment.')
            return redirect('blog_detail', slug=post.slug)
        if request.user.is_authenticated:
            author = request.user
        else:
            guest_name = request.POST.get('guest_name', 'Anonymous')
            author = None
        comment = Comment.objects.create(
            post=post,
            author=author,
            content=comment_content,
            guest_name=guest_name if not request.user.is_authenticated else None,
            is_approved=True
        )
        messages.success(request, 'Comment posted successfully!')
        return redirect('blog_detail', slug=post.slug)

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'excerpt', 'status']
    success_url = reverse_lazy('blog_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth.models import User
        from .models import Comment
        # Add all published blog posts to the context
        context['all_posts'] = BlogPost.objects.filter(status='published').order_by('-timestamp')
        context['user_count'] = User.objects.count()
        context['comment_count'] = Comment.objects.count()
        return context

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'excerpt', 'status']
    success_url = reverse_lazy('blog_list')
    
    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')
    
    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user) 

class UserRegistrationView(APIView):
    """User registration endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    """User login endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Please provide both username and password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED) 

class RegisterView(TemplateView):
    """User registration page"""
    template_name = 'registration/register.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        context = {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }
        # Basic validation
        if not username or not email or not password:
            context['error'] = 'Please fill in all required fields.'
            return render(request, self.template_name, context)
        if User.objects.filter(username=username).exists():
            context['error'] = 'Username already exists.'
            return render(request, self.template_name, context)
        if User.objects.filter(email=email).exists():
            context['error'] = 'Email already exists.'
            return render(request, self.template_name, context)
        # Create user
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=make_password(password)
        )
        messages.success(request, 'Registration successful! You can now log in.')
        return redirect('user_login')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class CustomLoginView(TemplateView):
    """Custom login view that handles both AJAX and regular form submissions"""
    template_name = 'registration/login.html'
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # next_url = request.POST.get('next') or request.GET.get('next')
        
        if not username or not password:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'error': 'Please provide both username and password'}, status=400)
            else:
                context = self.get_context_data()
                context['error'] = 'Please provide both username and password'
                return render(request, self.template_name, context)
        
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': True, 'redirect': '/create/'})
            else:
                return redirect('blog_create')
        else:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
            else:
                context = self.get_context_data()
                context['error'] = 'Invalid credentials'
                return render(request, self.template_name, context)
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

class WelcomeView(TemplateView):
    template_name = 'blog/welcome.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.contrib.auth.models import User
        from .models import BlogPost, Comment
        context['total_posts'] = BlogPost.objects.filter(status='published').count()
        context['total_users'] = User.objects.count()
        context['total_comments'] = Comment.objects.count()
        return context

    # Remove the get() override so it always shows the welcome page 