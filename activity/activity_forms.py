#encoding=utf-8

import logging

from django import forms
from DjangoUeditor.forms import UEditorField
from activity.models import ActivityCat, Area


class ActivityForm(forms.Form):
    category_list = ()
    categorys = ActivityCat.objects.all()
    for category in categorys:
        categorys_tuple = (category.id, category.name)
        category_list += (categorys_tuple,)

    title = forms.CharField(label="活动标题", max_length=64)
    category = forms.IntegerField(widget=forms.Select(choices=category_list))
    position = forms.CharField(label='活动地点', max_length=200)
    tags = forms.ModelMultipleChoiceField(queryset=Area.objects.all(), widget=forms.Select())
    acttime = forms.CharField(label='活动时间', max_length=200)
    excerpt = forms.CharField(label='活动摘要', max_length=200)
    company = forms.CharField(label='主办单位', max_length=200)
    author = forms.CharField(label='活动发起人', max_length=70)
    actfee = forms.CharField(label='活动费用', max_length=70)
    person = forms.CharField(label='人数上限', max_length=70)
    is_help = forms.CharField(initial=2, widget=forms.Select(choices=((True, '需要'), (False, '不需要'),)))
    img = forms.ImageField(label='活动图片')
    content = UEditorField(label='文章内容', width=800, height=900,
                           toolbars="full", imagePath="upimg/", filePath="upfile/",
                           upload_settings={"imageMaxSize": 1204000},
                           settings={})

    def __init__(self, *args, **kw):
        super(ActivityForm, self).__init__(*args, **kw)
