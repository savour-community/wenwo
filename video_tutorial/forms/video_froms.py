#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from video_tutorial.models import Video, VideoCategory, Charpter
from mdeditor.fields import MDTextFormField
from common.helpers import dec, d0


class VideoForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="视频课程标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入视频课程标题", "class": "form-control"}
        ),
        error_messages={"required": "请输入视频课程标题, 视频课程标题不能为空"},
    )
    excerpt = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入视频课程摘要'
            }
        )
    )
    category = forms.ModelChoiceField(
        empty_label="请选择课程类别",
        queryset=VideoCategory.objects.filter(is_active=True)
    )
    video_img = forms.ImageField(
        required=True,
        error_messages={"invalid": "请上传图片, 图片不能为空"},
    )
    video_intro = MDTextFormField()
    price = forms.CharField(
        required=True,
        label="视频课程价格",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入视频课程价格", "class": "form-control"}
        ),
        error_messages={"required": "请输入视频课程价格, 视频课程价格不能为空"},
    )
    level = forms.CharField(
        initial=4,
        widget=forms.Select(
            choices=(('Rookie', 'Rookie'), ('Primary', 'Primary'), ('Middle', 'Middle'), ('Senior', 'Senior'),)
        )
    )

    class Meta:
        model = Video
        fields = [
            'title', 'excerpt', 'category', 'video_img', 'video_intro', 'price', 'level'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(VideoForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('视频标题不能为空')
        return title

    def clean_excerpt(self):
        excerpt = self.cleaned_data.get('excerpt')
        if excerpt in ['', None]:
            raise forms.ValidationError('视频摘要不能为空')
        return excerpt

    def clean_category(self):
        category = self.cleaned_data.get('category')
        return category

    def clean_video_img(self):
        video_img = self.cleaned_data.get('video_img')
        return video_img

    def clean_video_intro(self):
        video_intro = self.cleaned_data.get('video_intro')
        if video_intro in ['', None]:
            raise forms.ValidationError('视频内容不能为空')
        return video_intro

    def clean_price(self):
        price = dec(self.cleaned_data.get('price'))
        if price < 0:
            raise forms.ValidationError('课程价格无效，情输入大于等于0的数字')
        return price

    def clean_level(self):
        level = self.cleaned_data.get('level')
        return level

    def create_video(self, user):
        Video.objects.create(
            title=self.clean_title(),
            excerpt=self.clean_excerpt(),
            category=self.clean_category(),
            video_img=self.clean_video_img(),
            video_intro=self.clean_video_intro(),
            price=dec(self.clean_price()),
            user=user,
            level=self.clean_level(),
        )

    def update_video(self, vid):
        video = Video.objects.filter(id=vid).first()
        video.title = self.clean_title()
        video.excerpt = self.clean_excerpt()
        video.category = self.clean_category()
        video.video_img = self.clean_video_img()
        video.video_intro = self.clean_video_intro()
        video.price = self.clean_price()
        video.level = dec(self.clean_level())
        video.status = 'Checking'
        video.save()
