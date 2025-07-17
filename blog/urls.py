from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView

router = DefaultRouter()
router.register(r'posts', views.BlogPostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'likes', views.LikeViewSet)

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.UserRegistrationView.as_view(), name='user_register'),
    path('api/login/', views.UserLoginView.as_view(), name='user_login'),
    
    # Frontend URLs
    path('', views.WelcomeView.as_view(), name='welcome'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('post/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('edit/<int:pk>/', views.BlogUpdateView.as_view(), name='blog_edit'),
    path('delete/<int:pk>/', views.BlogDeleteView.as_view(), name='blog_delete'),
    
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(next_page='welcome'), name='user_logout'),
    path('register/', views.RegisterView.as_view(), name='user_register'),
] 