#encoding=utf-8

import logging
from django import forms
from video_tutorial.models import Video, VideoCategory, Charpter
from common.helpers import dec, d0


class CharpterForm(forms.Form):
    chart = forms.CharField(
        required=True,
        label="视频章节",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入视频章节", "class": "form-control"}
        ),
        error_messages={"required": "请输入视频章节, 视频章节不能为空"},
    )
    chart_name = forms.CharField(
        required=True,
        label="章节名称",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入章节名称", "class": "form-control"}
        ),
        error_messages={"required": "请输入章节名称, 章节名称不能为空"},
    )
    video_url = forms.CharField(
        required=True,
        label="章节名称",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入视频URL", "class": "form-control"}
        ),
        error_messages={"required": "请输入视频URL, 视频URL不能为空"},
    )

    def __init__(self, request, *args, **kw):
        self.request = request
        super(CharpterForm, self).__init__(*args, **kw)

    def clean_chart(self):
        chart = self.cleaned_data.get('chart')
        if chart in ['', None]:
            raise forms.ValidationError('视频章节不能为空')
        return chart

    def clean_chart_name(self):
        chart_name = self.cleaned_data.get('chart_name')
        if chart_name in ['', None]:
            raise forms.ValidationError('章节名称不能为空')
        return chart_name

    def clean_video_url(self):
        video_url = self.cleaned_data.get('video_url')
        if video_url in ['', None]:
            raise forms.ValidationError('视频URL不能为空')
        return video_url


