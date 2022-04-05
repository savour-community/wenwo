#encoding=utf-8

from django.db import models
from wenwo.models import BaseModel
from DjangoUeditor.models import UEditorField
from wenwo_auth.models import User


SuggestChoice = [(x, x) for x in ['Accept', 'Refuse', 'UnHandle']]


class Suggestion(BaseModel):
    title = models.CharField(max_length=70, verbose_name='反馈标题')
    body = UEditorField(
        width=800, height=500,
        toolbars="full", imagePath="upimg/", filePath="upfile/",
        upload_settings={"imageMaxSize": 1204000},
        settings={}, command=None, blank=True,
        verbose_name='反馈内容'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='反馈的用户')
    status = models.CharField(
        max_length=100,
        choices=SuggestChoice,
        default="UnHandle",
        verbose_name="状态",
    )
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '建议反馈表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Notice(BaseModel):
    title = models.CharField(max_length=70, verbose_name='公告标题')
    excerpt = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='公告摘要'
    )
    content = UEditorField(
        width=800, height=500,
        toolbars="full", imagePath="upimg/", filePath="upfile/",
        upload_settings={"imageMaxSize": 1204000},
        settings={}, command=None, blank=True,
        verbose_name='公告内容'
    )
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '公告表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


