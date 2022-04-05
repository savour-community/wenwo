#encoding=utf-8

import pytz
from django.db import models
from wenwo_auth.models import User, UserInfo
from DjangoUeditor.models import UEditorField
from wenwo.models import BaseModel
from mdeditor.fields import MDTextField
from django.conf import settings


tz = pytz.timezone(settings.TIME_ZONE)


PlatformsChoice = [
    (x, x) for x in ["All", "Ios", "Android", "WeiChat"]
]
YesOrNo =  [
    (x, x) for x in ["Yes", "No", "Unknown"]
]


class Helper(BaseModel):
    title = models.CharField(
        max_length=100,
        verbose_name='标题'
    )
    detail = MDTextField(
        null=True,
        blank=True,
        verbose_name='内容'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='是否是有效'
    )

    class Meta:
        verbose_name = '常见问题表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }


class Version(BaseModel):
    version_num = models.CharField(
        max_length=100,
        verbose_name='版本号'
    )
    platforms = models.CharField(
        max_length=100,
        choices=PlatformsChoice,
        default="Android",
        verbose_name='安装平台'
    )
    detail = MDTextField(
        null=True,
        blank=True,
        verbose_name='版本描述'
    )
    download_url = models.CharField(
        max_length=100,
        verbose_name='下载地址'
    )
    is_force = models.CharField(
        max_length=100,
        choices=YesOrNo,
        default="All",
        verbose_name='是否强制更新'
    )

    class Meta:
        verbose_name = '版本号表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.version_num

    def to_dict(self):
        return {
            'id': self.id,
            'version_num': self.version_num,
            'platforms': self.platforms,
            'detail': self.detail,
            'download_url': self.download_url,
            'is_force': self.is_force,
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }
