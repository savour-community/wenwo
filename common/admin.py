from django.contrib import admin
from common.models import Helper, Version


@admin.register(Helper)
class HelperAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_active')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'version_num', 'platforms', 'is_force')