#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from book.models import CourseCommet
from mdeditor.fields import MDTextFormField


class CourseCommetForm(forms.ModelForm):
    content = MDTextFormField()

    class Meta:
        model = CourseCommet
        fields = [
            'content'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(CourseCommetForm, self).__init__(*args, **kw)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content in ['', None]:
            raise forms.ValidationError('评论内容不能为空')
        return content

    def create_comment(self, course, course_chapter, user):
        CourseCommet.objects.create(
            course=course,
            user=user,
            artcle=course_chapter,
            content=self.clean_content()
        )








