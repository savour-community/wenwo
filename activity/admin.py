#encoding=utf-8

from django.contrib import admin
from activity.models import (
    Activity
)


@admin.register(Activity)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'company', 'author', 'views')
    list_per_page = 50
    ordering = ('-id',)
    list_display_links = ('id', 'title')


