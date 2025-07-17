from django.contrib import admin
from django.utils.html import format_html
from .models import BlogPost, Comment, Like

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'timestamp', 'like_count', 'comment_count']
    list_filter = ['status', 'timestamp', 'author']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['timestamp', 'updated_at', 'like_count', 'comment_count', 'likes_list', 'comments_list']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'excerpt', 'slug')
        }),
        ('Metadata', {
            'fields': ('author', 'status', 'timestamp', 'updated_at')
        }),
        ('Statistics', {
            'fields': ('like_count', 'comment_count'),
            'classes': ('collapse',)
        }),
        ('Likes & Comments', {
            'fields': ('likes_list', 'comments_list'),
            'classes': ('collapse',)
        }),
    )
    
    def like_count(self, obj):
        return obj.like_count
    like_count.short_description = 'Likes'
    
    def comment_count(self, obj):
        return obj.comment_count
    comment_count.short_description = 'Comments'
    
    def likes_list(self, obj):
        likes = obj.likes.all()
        if likes:
            return format_html('<br>'.join([f"• {like.user.username} ({like.created_at.strftime('%Y-%m-%d %H:%M')})" for like in likes]))
        return "No likes"
    likes_list.short_description = 'Who Liked'
    
    def comments_list(self, obj):
        comments = obj.comments.all()
        if comments:
            comment_list = []
            for comment in comments:
                author_name = comment.display_name
                status = "✓" if comment.is_approved else "⏳"
                comment_list.append(f"• {status} {author_name}: {comment.content[:50]}... ({comment.created_at.strftime('%Y-%m-%d %H:%M')})")
            return format_html('<br>'.join(comment_list))
        return "No comments"
    comments_list.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author_display', 'content_preview', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at', 'author']
    search_fields = ['content', 'author__username', 'guest_name', 'post__title']
    readonly_fields = ['created_at']
    actions = ['approve_comments', 'disapprove_comments']
    
    def author_display(self, obj):
        return obj.display_name
    author_display.short_description = 'Author'
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Disapprove selected comments"

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['post__title', 'user__username']
    readonly_fields = ['created_at'] 