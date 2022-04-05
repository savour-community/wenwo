#encoding=utf-8

import pytz
from django.db import models
from wenwo_auth.models import User, UserInfo
from DjangoUeditor.models import UEditorField
from wenwo.models import BaseModel
from mdeditor.fields import MDTextField
from django.conf import settings


tz = pytz.timezone(settings.TIME_ZONE)


BlogCheck = [(x, x) for x in ['Yes', 'No']]


class Category(BaseModel):
    name = models.CharField(max_length=100, verbose_name='分类名称')
    index = models.IntegerField(default=999, verbose_name='分类索引')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '类别表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_active": self.is_active
        }


class Tag(BaseModel):
    name = models.CharField(max_length=100, verbose_name='名称')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '标签表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tui(BaseModel):
    name = models.CharField(max_length=100, verbose_name='名称')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '推荐表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(BaseModel):
    title = models.CharField(max_length=70, verbose_name='标题', db_index=True)
    excerpt = models.TextField(max_length=200, null=True, blank=True, verbose_name='摘要')
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name = '类别'
    )
    tags = models.ManyToManyField(Tag, blank=True, null=True, verbose_name='标签')
    img = models.ImageField(upload_to='article_img/%Y/%m/%d/', blank=True, null=True)
    body = MDTextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='用户'
    )
    views = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    cmts = models.PositiveIntegerField(default=0, verbose_name='评论次数')
    like = models.PositiveIntegerField(default=0, verbose_name='点赞次数')
    tui = models.ForeignKey(
        Tui, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='是否推荐'
    )
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    is_check = models.CharField(max_length=100, choices=BlogCheck, default="No")
    is_active = models.BooleanField(default=True, verbose_name='是否有效')
    is_sync = models.BooleanField(default=False, verbose_name='是否已同步')

    class Meta:
        verbose_name = '文章表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_user_photo(self):
        try:
            user_info = UserInfo.objects.filter(user_id=self.user.id)
            if user_info is not None:
                return str(user_info.user_pho)
            else:
                return ""
        except:
            return ""

    def list_to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author_name": self.user.user_name,
            "author_pho": self.get_user_photo(),
            "excerpt": self.excerpt,
            "img": str(self.img),
            "views": self.views,
            "cmts": self.cmts,
            "like": self.like,
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }

    def get_author_info(self):
        try:
            user_info = UserInfo.objects.filter(user_id=self.user.id).first()
            return {
                "user_name": self.user.user_name,
                "user_photo": str(user_info.user_pho),
                "position": user_info.user_pos,
                "is_focus": False
            }
        except:
            return {
                "user_name": self.user.user_name,
                "user_photo": "",
                "position": "",
                "is_focus": False
            }

    def get_comment_reply(self):
        blog_reply_list = BlogReply.objects.filter(arcticle__id=self.id, reply_id=0).order_by("-id")[0:10]
        blog_reply_date = []
        for blog_reply in blog_reply_list:
            blog_reply_date.append(blog_reply.to_dict())
        return blog_reply_date

    def detail_to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "user": self.get_author_info(),
            "excerpt": self.excerpt,
            "body": self.body,
            "img": str(self.img),
            "views": self.views,
            "cmts": self.cmts,
            "comment": self.get_comment_reply(),
            "like": self.like,
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }


class BlogReply(BaseModel):
    arcticle = models.ForeignKey(
        Article, related_name="arcticle_blog_reply", on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='问题'
    )
    reply_id = models.IntegerField(default=0, verbose_name='回复ID')
    like = models.PositiveIntegerField(default=0, verbose_name='点赞次数')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='评论人')
    content = MDTextField()
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '评论回复表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

    def get_user(self):
        user_info = UserInfo.objects.filter(user_id=self.user.id).first()
        return {
            "user_name": self.user.user_name,
            "user_photo": str(user_info.user_pho),
            "position": user_info.user_pos,
            "is_focus": False
        }

    def get_reply(self, id):
        reply_data = []
        br_list = BlogReply.objects.filter(reply_id=id).order_by("-id")
        for br in br_list:
            reply_data.append(br.to_dict())
        return reply_data

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.get_user(),
            "content": self.content,
            "like": self.like,
            "reply_num": 0 if self.reply_id == 0 else BlogReply.objects.filter(reply_id=self.reply_id).count(),
            "reply_data": self.get_reply(self.id),
            "is_active": self.is_active,
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }
