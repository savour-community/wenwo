#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from about.models import Suggestion


class SuggestForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="文章标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入反馈标题", "class": "form-control"}
        ),
        error_messages={"required": "请输入反馈标题, 反馈标题不能为空"},
    )
    body = UEditorField(
        label='反馈内容', width=700, height=800,
        toolbars="full",
        imagePath="upimg/",
        filePath="upfile/",
        upload_settings={"imageMaxSize": 1204000}, settings={}
    )

    class Meta:
        model = Suggestion
        fields = [
            'title', 'body'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(SuggestForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('反馈标题不能为空')
        return title

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body in ['', None]:
            raise forms.ValidationError('反馈内容不能为空')
        return body

    def create_suggestion(self, user):
        article = Suggestion.objects.create(
            title=self.clean_title(),
            user=user,
            body=self.clean_body()
        )


