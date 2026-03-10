from django.contrib import admin

from user.models import Friendship
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author', 'content')

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at')
    list_filter = ('created_at',)
