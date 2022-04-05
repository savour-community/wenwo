#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from topic.models import TopicReply
from mdeditor.fields import MDTextFormField


class TopicReplyForm(forms.ModelForm):
    content = MDTextFormField()

    class Meta:
        model = TopicReply
        fields = [
            'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(TopicReplyForm, self).__init__(*args, **kw)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content in ['', None]:
            raise forms.ValidationError('评论内容不能为空')
        return content

    def create_comment(self, topic, reply_id, user):
        TopicReply.objects.create(
            topic=topic,
            reply_id=reply_id,
            user=user,
            content=self.clean_content()
        )








