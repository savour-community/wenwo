#encoding=utf-8

import logging
from django.core import serializers
from django.http import JsonResponse
from django.db.models import F
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from topic.models import (
    TopicCategory,
    Topic,
    TopicReply)

from common.helpers import (
    paged_items,
    ok_json,
    error_json)
from topic.froms import TopicForm
from django.shortcuts import redirect


def send_topic(request):
    if request.method == 'GET':
        form = TopicForm()
        return render(request, 'frontend/wenwo_auth/send_topic.html', locals())
    elif request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            excerpt = form.cleaned_data.get('excerpt')
            category_id = form.cleaned_data.get('category')
            content = form.cleaned_data.get('content')
            account_id = request.session.get('user_id')
            account_name = request.session.get('user_name')
            category = TopicCategory.objects.get(id=category_id)
            article = Topic.objects.create(
                title=title,
                excerpt=excerpt,
                category=category,
                account_id=account_id,
                account_name=account_name,
                user_id=1,
                content=content)
        return redirect('/topic_list')
    else:
        return redirect('/topic_list')


# 话题列表
def topic_list(request):
    lid = request.GET.get('lid', 'all')
    page = request.GET.get('page', 0)
    logging.info("category name is %s and page is %s", lid, page)
    tcat_list = TopicCategory.objects.all()
    topic_lists = Topic.objects.all()
    hot_topic_list = Topic.objects.all().order_by('-like')[0:10]
    if lid not in ['all', '', '0', 0,  None]:
        topic_lists = topic_lists.filter(category_id=lid)
    topic_lists = topic_lists.order_by('-id')
    paginator = Paginator(topic_lists, 100)
    try:
        topic_list = paginator.page(page)
    except PageNotAnInteger:
        topic_list = paginator.page(1)
    except EmptyPage:
        topic_list = paginator.page(paginator.num_pages)
    if request.is_ajax():
        json_data = serializers.serialize("json", topic_list, ensure_ascii=False)
        return ok_json({'topic_list': json_data})
    return render(request, 'frontend/topic/topic_list.html', locals())


# 话题详情
def topic_detail(request, tid):
    logging.info("topic id is %s", tid)

    topic_show = Topic.objects.get(id=tid)
    hot_topic_list = Topic.objects.all().order_by('-like')[0:10]

    topic_reply_lists = TopicReply.objects.filter(topic_id=tid).order_by('-id')

    topic_reply_num = len(topic_reply_lists)
    topic_show.views = topic_show.views + 1
    topic_show.save()

    topic_reply_list = paged_items(request, topic_reply_lists)
    if request.is_ajax():
        json_data = serializers.serialize("json", topic_reply_list, ensure_ascii=False)
        return ok_json({'topic_reply': json_data})
    return render(request, 'frontend/topic/topic_detail.html', locals())


def set_comment_reply(request):
    topic_id = request.POST.get("topic_id")
    reply_id = request.POST.get("reply_id")
    account_id = request.POST.get("account_id")
    content = request.POST.get("content")
    account_name = request.session.get('user_name')
    if content in ["", None]:
        return error_json("回复的内容不能为空", 1000)
    else:
        try:
            TopicReply.objects.create(
                topic_id=topic_id,
                reply_id=reply_id,
                account_id=account_id,
                account_name=account_name,
                user_id=1,
                content=content)
            return ok_json("评论成功")
        except:
            return error_json("评论失败,请检查是否已经登陆", 1000)


# 话题点赞
def topic_like(request):
    topic_id = request.GET.get("id")
    logging.info("topic id is %s", topic_id)
    Topic.objects.filter(id=topic_id).update(like=F('like') + 1)
    topic_model = Topic.objects.filter(id=topic_id).values('like')
    total_like = topic_model[0]['like']
    return JsonResponse({'total_like': total_like})


def comment_like(request):
    reply_id = request.GET.get("id")
    logging.info("topic id is %s", reply_id)
    TopicReply.objects.filter(id=reply_id).update(like=F('like') + 1)
    topic_reply = TopicReply.objects.filter(id=reply_id).values('like')
    topic_reply_like = topic_reply[0]['like']
    return JsonResponse({'topic_reply_like': topic_reply_like})







