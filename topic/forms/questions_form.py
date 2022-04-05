#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from topic.models import Topic, TopicCategory
from mdeditor.fields import MDTextFormField


class TopicForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="问题标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入问题标题", "class": "form-control"}
        ),
        error_messages={"required": "请输入问题标题, 问题标题不能为空"},
    )
    category = forms.ModelChoiceField(
        empty_label="请选择问题类别",
        queryset=TopicCategory.objects.all()
    )
    content = MDTextFormField()

    class Meta:
        model = Topic
        fields = [
            'title', 'category', 'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(TopicForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            return self.add_error('title', '标题不能为空')
        return title

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category in ['', None]:
            return self.add_error('category', '分类必须要选择')
        return category

    def clean_content(self):
        content = self.cleaned_data.get('content')
        return content

    def create_question(self, user):
        Topic.objects.create(
            title=self.clean_title(),
            category=self.clean_category(),
            user=user,
            content=self.clean_content()
        )





