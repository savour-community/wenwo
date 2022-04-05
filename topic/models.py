#encoding=utf-8


import pytz
from django.db import models
from wenwo_auth.models import User
from DjangoUeditor.models import UEditorField
from wenwo.models import BaseModel
from mdeditor.fields import MDTextField
from django.conf import settings


tz = pytz.timezone(settings.TIME_ZONE)


class TopicCategory(BaseModel):
    name = models.CharField(max_length=100, verbose_name='分类名称')
    index = models.IntegerField(default=999, verbose_name='分类索引')

    class Meta:
        verbose_name = '贴吧分类表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "index": self.index,
        }


class Topic(BaseModel):
    TopicCheck = [(x, x) for x in ['Yes', 'No']]
    title = models.CharField(max_length=70, verbose_name='分类名称')
    excerpt = models.TextField(max_length=200, blank=True, verbose_name='分类名称')
    category = models.ForeignKey(
        TopicCategory,
        on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='分类名称'
    )
    content = MDTextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='提问人'
    )
    like = models.PositiveIntegerField(
        default=0,
        verbose_name='点赞人数'
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name='查看次数'
    )
    answers = models.PositiveIntegerField(
        default=0,
        verbose_name='回答次数'
    )
    is_check = models.CharField(
        max_length=100,
        choices=TopicCheck,
        default="No"
    )

    class Meta:
        verbose_name = '贴吧表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_user_info(self):
        try:
            user_info = UserInfo.objects.filter(user_id=self.user.id).first()
            return {
                "user_name": self.user.user_name,
                "user_photo": str(user_info.user_pho),
                "is_focus": False
            }
        except:
            return {
                "user_name": self.user.user_name,
                "user_photo": "",
                "is_focus": False
            }

    def list_to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "excerpt": self.excerpt,
            "category": self.category.name,
            "content": self.content,
            "user": self.get_user_info(),
            "like": self.like,
            "views": self.views,
            "answers": self.answers,
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }

    def get_reply(self):
        topic_reply_list = TopicReply.objects.filter(topic=self, reply_id=0).order_by("-id")
        topic_return_data = []
        for topic_reply in topic_reply_list:
            topic_return_data.append(topic_reply.to_dict())
        return topic_return_data

    def detail_to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "excerpt": self.excerpt,
            "category": self.category.name,
            "content": self.content,
            "user": self.get_user_info(),
            "like": self.like,
            "views": self.views,
            "answers": self.answers,
            "reply": self.get_reply(),
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }


class TopicReply(BaseModel):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.DO_NOTHING,
        blank=True, null=True,
        verbose_name='贴吧'
    )
    reply_id = models.IntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = MDTextField()

    class Meta:
        verbose_name = '贴吧评论回复'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

    def get_user_info(self):
        try:
            user_info = UserInfo.objects.filter(user_id=self.user.id).first()
            return {
                "user_name": self.user.user_name,
                "user_photo": str(user_info.user_pho),
                "is_focus": False
            }
        except:
            return {
                "user_name": self.user.user_name,
                "user_photo": "",
                "is_focus": False
            }

    def get_reply(self):
        tr_list = TopicReply.objects.filter(reply_id=self.id).order_by("-id")
        tr_return_data = []
        for tr in tr_list:
            tr_return_data.append(tr.to_dict())
        return tr_return_data

    def to_dict(self):
        return {
            "id": self.id,
            "reply_id": self.reply_id,
            "like": self.like,
            "user": self.get_user_info(),
            "content": self.content,
            "reply": self.get_reply(),
            "created_at": self.created_at.astimezone(tz).strftime('%Y-%m-%d %H:%M'),
        }




