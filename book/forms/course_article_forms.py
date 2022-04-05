#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from book.models import CourseArtcle, Course
from mdeditor.fields import MDTextFormField
from common.helpers import dec, d0


class CourseArtcleForm(forms.ModelForm):
    part = forms.CharField(
        required=True,
        label="文章章节",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入文章章节", "class": "form-control"}
        ),
        error_messages={"required": "请输入文章章节, 文章章节不能为空"},
    )
    title = forms.CharField(
        required=True,
        label="文章标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入文章标题", "class": "form-control"}
        ),
        error_messages={"required": "请输入文章标题, 文章标题不能为空"},
    )
    detail = MDTextFormField(required=False)

    class Meta:
        model = CourseArtcle
        fields = [
            'part', 'title', 'detail'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(CourseArtcleForm, self).__init__(*args, **kw)

    def clean_part(self):
        part = self.cleaned_data.get('part')
        if part in ['', None]:
            raise forms.ValidationError('文章章节不能为空')
        return part

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('文章标题不能为空')
        return title

    def clean_detail(self):
        detail = self.cleaned_data.get('detail')
        return detail

    def create_article(self, cid):
        course = Course.objects.filter(id=cid).first()
        CourseArtcle.objects.create(
            part=self.clean_part(),
            title=self.clean_title(),
            course=course,
            detail=self.clean_detail(),
            is_free='Yes',
        )
        course.article_num += 1
        course.save()

    def update_article(self, aid):
        article = CourseArtcle.objects.filter(id=aid).first()
        article.part = self.clean_part()
        article.title = self.clean_title()
        article.detail = self.clean_detail()
        article.status = 'Checking'
        article.save()











