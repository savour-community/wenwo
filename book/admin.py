from django.contrib import admin
from book.models import (
    Course,
    CourseCat,
    CourseArtcle,
    CourseCommet
)


@admin.register(CourseCat)
class CourseCatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'views', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')


@admin.register(CourseArtcle)
class CharpterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'comment_num')


@admin.register(CourseCommet)
class VideoReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'content')




