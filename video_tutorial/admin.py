from django.contrib import admin
from video_tutorial.models import (
    VideoCategory,
    Video,
    VideoReply,
    Charpter
)

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'user', 'views', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')


@admin.register(VideoReply)
class VideoReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'like')


@admin.register(Charpter)
class CharpterAdmin(admin.ModelAdmin):
    list_display = ('id', 'chart', 'chart_name')



