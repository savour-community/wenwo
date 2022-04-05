#encoding=utf-8

import logging
from django.shortcuts import render
from django.shortcuts import redirect
from activity.models import (
    Activity
)


def activity_list(request):
    nav_cat = "activity"
    activity_list = Activity.objects.all()
    return render(request, 'v2_front/activity/activity_list.html', locals())


def activity_detail(request,sid):
    activity_show = Activity.objects.get(id=sid)
    hot_activity = Activity.objects.all().order_by('?')[:10]
    activity_show.views = activity_show.views + 1
    activity_show.save()
    return render(request, 'v2_front/activity/activity_detail.html', locals())