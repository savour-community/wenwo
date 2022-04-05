#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from blog.models import BlogReply
from mdeditor.fields import MDTextFormField


class BlogReplyForm(forms.ModelForm):
    content = MDTextFormField()

    class Meta:
        model = BlogReply
        fields = [
            'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(BlogReplyForm, self).__init__(*args, **kw)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content in ['', None]:
            raise forms.ValidationError('评论内容不能为空')
        return content

    def create_comment(self, arcticle, reply_id, user):
        BlogReply.objects.create(
            arcticle=arcticle,
            reply_id=reply_id,
            user=user,
            content=self.clean_content()
        )








