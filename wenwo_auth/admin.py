from django.contrib import admin
from wenwo_auth.models import (
    ApiAuth,
    User,
    UserInfo,
    Account,
    UserWallet,
    UserWalletRecord,
    Fans
)


@admin.register(ApiAuth)
class ApiAuthAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'api_token',
                    'is_expire')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'role',
                    'password')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_name',
                    'password',
                    'token',
                    'token_is_expire',
                    'phone')


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'user_real_name',
                    'user_pho',
                    'user_intro',
                    'user_sex',
                    'user_age',
                    'created_at',
                    'user_email',
                    'user_id',
                    'user_qq',
                    'user_wechat')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'user_real_name')


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'coin_type', 'amount')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'coin_type')


@admin.register(UserWalletRecord)
class UserWalletRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'coin_type', 'amount', 'source_type')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'coin_type')


@admin.register(Fans)
class FansAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    list_per_page = 50
    ordering = ('-created_at',)
    list_display_links = ('id', 'created_at')