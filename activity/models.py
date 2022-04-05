#encoding=utf-8

from django.db import models
from DjangoUeditor.models import UEditorField


class Activity(models.Model):
    title = models.CharField(max_length=70, verbose_name='活动标题')
    position = models.TextField(max_length=200, blank=True, verbose_name='活动地点')
    acttime = models.TextField(max_length=200, blank=True, verbose_name='活动时间')
    excerpt = models.TextField(max_length=200, blank=True, verbose_name='活动摘要')
    company = models.TextField(max_length=200, blank=True, verbose_name='主办单位')
    author = models.CharField(max_length=70, verbose_name='活动发起人')
    actfee = models.CharField(max_length=70, verbose_name='活动费用')
    person = models.CharField(max_length=70, verbose_name='人数上限')
    is_help = models.CharField(max_length=70, verbose_name='活动资助')
    img = models.ImageField(
        upload_to='article_img/%Y/%m/%d/',
        blank=True, null=True,
        verbose_name = '活动图片'
    )
    body = UEditorField(
        width=800, height=500,
        toolbars="full", imagePath="upimg/", filePath="upfile/",
        upload_settings={"imageMaxSize": 1204000},
        settings={}, command=None, blank=True,
        verbose_name='活动内容'
    )
    views = models.PositiveIntegerField(default=0, verbose_name='阅读量')
    is_active = models.BooleanField(default=True, verbose_name='是否是开启活动')

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = '活动'

    def __str__(self):
        return self.title
