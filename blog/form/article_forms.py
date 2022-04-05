#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from blog.models import Category, Article
from mdeditor.fields import MDTextFormField


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="文章标题",
        max_length=64,
        widget=forms.widgets.TextInput(
            {"placeholder": "请输入文章标题", "class": "form-control"}
        ),
        error_messages={"required": "请输入文章标题, 文章标题不能为空"},
    )
    excerpt =forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': '请输入文章摘要'
            }
        )
    )
    category = forms.ModelChoiceField(
        empty_label="请选择文章类别",
        queryset=Category.objects.filter(is_active=True)
    )
    body = MDTextFormField()

    class Meta:
        model = Article
        fields = [
            'title', 'excerpt', 'category', 'body'
        ]

    def __init__(self, request, *args, **kw):
        self.request = request
        super(ArticleForm, self).__init__(*args, **kw)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title in ['', None]:
            raise forms.ValidationError('文章标题不能为空')
        return title

    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body in ['', None]:
            raise forms.ValidationError('文章内容不能为空')
        return body

    def clean_excerpt(self):
        excerpt = self.cleaned_data.get('excerpt')
        if excerpt in ['', None]:
            raise forms.ValidationError('文章摘要不能为空')
        return excerpt

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category in ['', None]:
            raise forms.ValidationError('分类必须要选择')
        return category

    def create_blog(self, user):
        blogC = Article.objects.filter(title=self.clean_title(), user=user).order_by("-id").first()
        if blogC is None:
            Article.objects.create(
                title=self.clean_title(),
                excerpt=self.clean_excerpt(),
                category=self.clean_category(),
                user=user,
                body=self.clean_body()
            )
        else:
            blogC.title=self.clean_title()
            blogC.excerpt=self.clean_excerpt()
            blogC.category=self.clean_category()
            blogC.body=self.clean_body()
            blogC.save()

    def upate_blog(self, bid):
        article = Article.objects.filter(id=bid).first()
        article.title = self.clean_title()
        article.excerpt = self.clean_excerpt()
        article.category = self.clean_category()
        article.body = self.clean_body()
        article.save()











