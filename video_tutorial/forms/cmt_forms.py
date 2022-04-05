#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from video_tutorial.models import VideoReply
from mdeditor.fields import MDTextFormField


class VideoReplyForm(forms.ModelForm):
    content = MDTextFormField()

    class Meta:
        model = VideoReply
        fields = [
            'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(VideoReplyForm, self).__init__(*args, **kw)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content in ['', None]:
            raise forms.ValidationError('评论内容不能为空')
        return content

    def create_comment(self, video, reply_id, user):
        VideoReply.objects.create(
            video=video,
            reply_id=reply_id,
            user=user,
            content=self.clean_content()
        )








