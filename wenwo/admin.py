#encoding=utf-8

from django.contrib import admin
from .models import Banner,  Link


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_info', 'img', 'link_url', 'is_active')


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','linkurl')