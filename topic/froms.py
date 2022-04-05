#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from topic.models import TopicCategory


class TopicForm(forms.Form):
    category_list = ()
    categorys = TopicCategory.objects.all()
    for category in categorys:
        categorys_tuple = (category.id, category.name)
        category_list += (categorys_tuple, )
    title = forms.CharField(label="文章标题", max_length=64)
    excerpt = forms.CharField(label="文章摘要", max_length=200)
    category = forms.IntegerField(widget=forms.Select(choices=category_list))
    content = UEditorField('文章内容',
                           width=800, height=900,
                           toolbars="full", imagePath="upimg/", filePath="upfile/",
                           upload_settings={"imageMaxSize": 1204000},
                           settings={})

    def __init__(self, *args, **kw):
        super(TopicForm, self).__init__(*args, **kw)

