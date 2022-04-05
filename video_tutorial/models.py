#encoding=utf-8

from django.db import models
from wenwo_auth.models import User
from DjangoUeditor.models import UEditorField
from wenwo.models import BaseModel
from common.model_fields import DecField
from common.helpers import d0
from mdeditor.fields import MDTextField


LEVEL_CHOICE = [(x, x) for x in ['Rookie', 'Primary', 'Middle', 'Senior']]
VedioStatus = [
    (x, x) for x in ["Checking", "CheckFail", "CheckPass"]
]

class VideoCategory(BaseModel):
    name = models.CharField(max_length=100, verbose_name='分类名称')
    index = models.IntegerField(default=999, verbose_name='分类索引')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '视频类别表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "index": self.index,
        }


class Video(BaseModel):
    title = models.CharField(max_length=70, verbose_name='标题')
    excerpt = models.TextField(max_length=200, blank=True, verbose_name='摘要')
    category = models.ForeignKey(
        VideoCategory, on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='分类'
    )
    video_img = models.ImageField(
        upload_to='video_img/%Y/%m/%d/',
        blank=True, null=True,
        verbose_name='视频图片'
    )
    video_intro = MDTextField()
    price = DecField(default=d0, verbose_name='视频价格')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='发布人'
    )
    level = models.CharField(
        max_length=16, choices=LEVEL_CHOICE,
        default='Primary', verbose_name=u'级别'
    )
    status = models.CharField(
        max_length=100,
        choices=VedioStatus,
        default="Checking",
        verbose_name="视频教程状态",
    )
    check_reason = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='审核建议'
    )
    cmts=models.PositiveIntegerField(default=0, verbose_name='评论数')
    buyers=models.PositiveIntegerField(default=0, verbose_name='购买人数')
    views = models.PositiveIntegerField(default=0, verbose_name='查看次数')
    like = models.PositiveIntegerField(default=0, verbose_name='点赞次数')
    charpter_num = models.PositiveIntegerField(default=0, verbose_name='视频章节数量')
    process = models.CharField(max_length=100, default="0", verbose_name='完成度')
    is_active = models.BooleanField(default=True, verbose_name='是否是有效')

    class Meta:
        verbose_name = '视频表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_user(self):
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

    def get_chapter(self):
        chater_list = Charpter.objects.filter(video=self).order_by("-id")
        chapter_return_data = []
        for chapter in chater_list:
            chapter_return_data.append(chapter.to_dict())
        return chapter_return_data

    def get_comment(self):
        comment_list = VideoReply.objects.filter(video=self, reply_id=0).order_by("-id")
        comment_return_data = []
        for comment in comment_list:
            comment_return_data.append(comment.to_dict())
        return comment_return_data

    def detail_to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "excerpt": self.excerpt,
            "video_img": str(self.video_img),
            "video_intro": self.video_intro,
            "level": self.level,
            "cmts": self.cmts,
            "buyers": self.buyers,
            "views": self.views,
            "like": self.like,
            "charpter_num": self.charpter_num,
            "process": self.process,
            "user": self.get_user(),
            "chapter": self.get_chapter(),
            "comment": self.get_comment(),
            "is_active": self.is_active
        }

    def list_to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "excerpt": self.excerpt,
            "video_img": str(self.video_img),
            "views": self.views
        }


class Charpter(BaseModel):
    video = models.ForeignKey(
        Video,
        on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='关联视频'
    )
    status = models.CharField(
        max_length=100,
        choices=VedioStatus,
        default="Checking",
        verbose_name="视频教程状态",
    )
    check_reason = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='审核建议'
    )
    chart = models.IntegerField(default=0, verbose_name='章节数')
    views = models.PositiveIntegerField(default=0, verbose_name='查看次数')
    cmts = models.PositiveIntegerField(default=0, verbose_name='评论数')
    chart_name = models.CharField(max_length=70, default='', verbose_name='章节名称')
    video_url = models.CharField(max_length=70, default='', verbose_name='视频链接')
    time_long = models.CharField(max_length=70, default='10.00', verbose_name='视频时长')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '视频章节表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.chart_name

    def to_dict(self):
        return {
            "id": self.id,
            "chart": self.chart,
            "chart_name": self.chart_name,
            "video_url": self.video_url
        }


class VideoReply(BaseModel):
    video = models.ForeignKey(
        Video,
        on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='关联视频'
    )
    reply_id = models.IntegerField(default=0, verbose_name='回复ID')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name='评论用户'
    )
    like = models.PositiveIntegerField(default=0, verbose_name='点赞次数')
    content = MDTextField()
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '视频评论回复表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

    def get_user(self):
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

    def get_reply(self):
        vr_list = VideoReply.objects.filter(reply_id=self.id).order_by("-id")
        vr_return_data = []
        for vr in vr_list:
            vr_return_data.append(vr.to_dict())
        return vr_return_data

    def to_dict(self):
        return {
            "id": self.id,
            "like": self.like,
            "content": self.content,
            "user": self.get_user(),
            "reply": self.get_reply()
        }


class UserBuyVideo(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=u'购买人'
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='关联视频'
    )
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        verbose_name = '用户购买视频表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return ""

    def as_dict(self):
        return {
            'id': self.id
        }