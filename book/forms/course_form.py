#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from book.models import Course, CourseArtcle, CourseCat
from mdeditor.fields import MDTextFormField
from common.helpers import dec, d0


class CourseForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="课程标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入课程标题", "class": "form-control"}
        ),
        error_messages={"required": "请输入课程标题, 课程标题不能为空"},
    )
    logo = forms.ImageField(
        required=True,
        error_messages={"invalid": "请上传图片, 图片不能为空"},
    )
    excerpt =forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入课程摘要'
            }
        )
    )
    category = forms.ModelChoiceField(
        empty_label="请选择课程类别",
        queryset=CourseCat.objects.filter(is_active=True)
    )
    detail = MDTextFormField()
    price = forms.CharField(
        required=True,
        label="课程价格",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入课程价格", "class": "form-control"}
        ),
        error_messages={"required": "请输入课程价格, 课程价格不能为空"},
    )

    class Meta:
        model = Course
        fields = [
            'title', 'logo', 'excerpt', 'category', 'detail', 'price'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(CourseForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('课程标题不能为空')
        return title

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        return logo

    def clean_excerpt(self):
        excerpt = self.cleaned_data.get('excerpt')
        if excerpt in ['', None]:
            raise forms.ValidationError('课程摘要不能为空')
        return excerpt

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category in ['', None]:
            raise forms.ValidationError('课程分类必须要选择')
        return category

    def clean_detail(self):
        detail = self.cleaned_data.get('detail')
        if detail in ['', None]:
            raise forms.ValidationError('课程内容不能为空')
        return detail

    def clean_price(self):
        price = dec(self.cleaned_data.get('price'))
        if price < 0:
            raise forms.ValidationError('课程价格无效，情输入大于等于0的数字')
        return price

    def create_course(self, user):
        Course.objects.create(
            title=self.clean_title(),
            logo=self.clean_logo(),
            excerpt=self.clean_excerpt(),
            category=self.clean_category(),
            detail=self.clean_detail(),
            price=self.clean_price(),
            status='Checking',
            is_pre_sell='No',
            user=user
        )

    def update_course(self, cid):
        course = Course.objects.filter(id=cid).first()
        course.title = self.clean_title()
        course.logo = self.clean_logo()
        course.excerpt = self.clean_excerpt()
        course.category = self.clean_category()
        course.detail = self.clean_detail()
        course.price = self.clean_price()
        course.status = 'Checking'
        course.save()
