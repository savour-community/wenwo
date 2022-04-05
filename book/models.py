#encoding=utf-8

import pytz
from django.db import models
from common.model_fields import DecField
from wenwo.models import BaseModel
from wenwo_auth.models import User, UserInfo
from mdeditor.fields import MDTextField
from common.helpers import d0
from django.conf import settings


CourseStatus = [
    (x, x) for x in ["Checking", "CheckFail", "CheckPass"]
]
YesOrNo = [
    (x, x) for x in ["Yes", "No"]
]

tz = pytz.timezone(settings.TIME_ZONE)


class CourseCat(BaseModel):
    name = models.CharField(max_length=100, verbose_name='名称')
    is_active = models.BooleanField(default=True, verbose_name='是否是有效')

    class Meta:
        verbose_name = '课程分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def return_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'uuid': self.uuid,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Course(BaseModel):
    title = models.CharField(max_length=100, verbose_name='课程标题')
    logo = models.ImageField(
        upload_to='block_logo/%Y/%m/%d/', blank=True,
        default="block_logo/2021/05/06/1.jpeg", null=True,
        verbose_name='课程图片'
    )
    excerpt = models.TextField(max_length=200, blank=True, verbose_name='课程摘要')
    category = models.ForeignKey(
        CourseCat, related_name="course_cat", on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='课程分类'
    )
    detail = MDTextField(
        null=True, blank=True, verbose_name='课程介绍'
    )
    price = DecField(
        default=d0, verbose_name="课程价格"
    )
    status = models.CharField(
        max_length=100,
        choices=CourseStatus,
        default="Checking",
        verbose_name="课程状态",
    )
    is_pre_sell = models.CharField(
        max_length=100,
        choices=YesOrNo,
        default="Yes",
        verbose_name="是否预售",
    )
    check_reason = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='审核建议'
    )
    buyer_num = models.PositiveIntegerField(default=0, verbose_name='购买人数')
    article_num = models.PositiveIntegerField(default=0, verbose_name='课时数量')
    views = models.PositiveIntegerField(default=0, verbose_name='课程阅读量')
    process = models.CharField(max_length=100, default="0", verbose_name='课程完成度')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='作者')
    is_active = models.BooleanField(default=True, verbose_name='是否是有效')
    is_sync = models.BooleanField(default=False, verbose_name='是否已同步')

    class Meta:
        verbose_name = '课程表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def list_to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'logo': str(self.logo),
            'excerpt': self.excerpt,
            'views': self.views,
            "price": self.price,
            "article_num": self.article_num,
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }

    def get_user_info(self):
        try:
            user_info = UserInfo.objects.filter(user_id=self.user.id).first()
            return {
                "user_name": self.user.user_name,
                "user_photo": str(user_info.user_pho),
                "user_pos": user_info.user_pos
            }
        except:
            return {
                "user_name": self.user.user_name,
                "user_photo": "",
                "user_pos": "高级开发工程师"
            }

    def get_content(self):
        ca_list = CourseArtcle.objects.filter(course=self)
        ca_return_data = []
        for ca in ca_list:
            ca_return_data.append(ca.list_to_dict())
        return ca_return_data

    def get_comment(self):
        cmt_list = CourseCommet.objects.filter(course=self)
        cmt_return_data = []
        for cmt in cmt_list:
            cmt_return_data.append(cmt.list_to_dict())
        return cmt_return_data

    def detail_to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'logo': str(self.logo),
            'excerpt': self.excerpt,
            'user': self.get_user_info(),
            'views': self.views,
            "article_num": self.article_num,
            "detail": self.detail,
            "content": self.get_content(),
            "comment": self.get_comment(),
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }


class CourseArtcle(BaseModel):
    part = models.CharField(max_length=100, default="1", verbose_name='章节')
    title = models.CharField(max_length=100, verbose_name='文章标题')
    course = models.ForeignKey(
        Course, related_name="course_cs_arctcle", on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='所属课程'
    )
    detail = MDTextField(
        null=True, blank=True, verbose_name='文章详细'
    )
    is_free = models.CharField(
        max_length=100,
        choices=YesOrNo,
        default="No",
        verbose_name="课程状态",
    )
    status = models.CharField(
        max_length=100,
        choices=CourseStatus,
        default="Checking",
        verbose_name="课程状态",
    )
    check_reason = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='审核建议'
    )
    comment_num = models.PositiveIntegerField(default=0, verbose_name='文章阅读量')
    views = models.PositiveIntegerField(default=0, verbose_name='文章阅读量')
    like = models.PositiveIntegerField(default=0, verbose_name='文章点赞量')
    is_active = models.BooleanField(default=False, verbose_name='是否是有效')

    class Meta:
        verbose_name = '课程文章表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def list_to_dict(self):
        return {
            'id': self.id,
            'part': self.part,
            'title': self.title,
            'views': self.views,
            'comment_num': self.comment_num,
            'is_free': self.is_free,
        }

    def get_comment(self):
        cmt_list = CourseCommet.objects.filter(artcle=self)
        cmt_return_data = []
        for cmt in cmt_list:
            cmt_return_data.append(cmt.list_to_dict())
        return cmt_return_data

    def cac_dict(self):
        return {
            "id": self.id,
            "part": self.part,
            "title": self.title,
            "detail": self.detail,
            "views": self.views,
            "comment_num": self.comment_num,
            "is_free": self.is_free,
            "comment": self.get_comment(),
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }


class CourseCommet(BaseModel):
    course = models.ForeignKey(
        Course, related_name="course_comment", on_delete=models.DO_NOTHING,
        blank=True, null=True, verbose_name='评论的课程'
    )
    user = models.ForeignKey(
        User, related_name="course_user_comment", on_delete=models.CASCADE,
        blank=True, null=True, verbose_name='回答者'
    )
    artcle = models.ForeignKey(
        CourseArtcle, related_name="comment_course_artcle", on_delete=models.CASCADE,
        blank=True, null=True, verbose_name='评论的文章'
    )
    content = MDTextField()
    is_active = models.BooleanField('是否是有效', default=True)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = '课程评论'

    def __str__(self):
        return self.content

    def get_user_info(self):
        try:
            user_info = UserInfo.objects.filter(user_id=self.user.id).first()
            return {
                "user_name": self.user.user_name,
                "user_photo": str(user_info.user_pho),
            }
        except:
            return {
                "user_name": self.user.user_name,
                "user_photo": "",
            }

    def list_to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user': self.get_user_info()
        }