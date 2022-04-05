#encoding=utf-8

from django.contrib import admin
from about.models import Suggestion, Notice


@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('id',  'title', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id',  'title', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'title')