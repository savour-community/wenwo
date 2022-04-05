from django.contrib import admin
from topic.models import (
    TopicCategory,
    Topic,
    TopicReply
)


@admin.register(TopicCategory)
class TopicCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'user', 'views', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')


@admin.register(TopicReply)
class TopicReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic_id', 'like', 'content')