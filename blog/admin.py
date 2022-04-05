from django.contrib import admin
from blog.models import Category, Tag, Tui, Article, BlogReply


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Tui)
class TuiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'tui', 'user', 'views', 'created_at')
    list_per_page = 50
    ordering = ('-created_time',)
    list_display_links = ('id', 'title')


@admin.register(BlogReply)
class BlogReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'reply_id', 'like', 'user', 'content')
    list_per_page = 50
    ordering = ('-id',)
    list_display_links = ('id', 'content')
