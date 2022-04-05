#encoding=utf-8

import logging
from django.shortcuts import render
from django.shortcuts import redirect
from wenwo_auth.models import (
    User,
    UserInfo,
    Fans,
    UserWallet,
    UserWalletRecord
)
from blog.models import Article
from topic.models import Topic
from book.models import Course
from video_tutorial.models import Video
from common.helpers import paged_items


def author_order(request):
    user_order_list = User.objects.all().order_by("-is_sign", "-login_times")
    user_id = request.session.get('user_id')
    rank = 1
    for user_order in user_order_list:
        user_info = UserInfo.objects.filter(user_id=user_order.id).first()
        if user_info is not None:
            user_order.user_pho = user_info.user_pho
            user_order.user_pos = user_info.user_pos
        user_order.blog_num =Article.objects.filter(user=user_order).count()
        user_order.topic_num = Topic.objects.filter(user=user_order).count()
        user_order.course_num = Course.objects.filter(user=user_order).count()
        user_order.video_num = Video.objects.filter(user=user_order).count()
        user_order.rank = rank
        fans = Fans.objects.filter(fans__id=user_order.id).first()
        if fans is not None:
            if fans.me.id == user_id:
                user_order.is_focus = True
        else:
            user_order.is_focus = False
        rank += 1
    user_order_list = paged_items(request, user_order_list)
    return render(request, 'v2_front/author/order.html', locals())


def author_main(request, uid):
    tab_active = "author_main"
    author_id = int(uid)
    if author_id == request.session.get('user_id'):
        return redirect('person_info')
    user = User.objects.filter(id=author_id).first()
    user_info = UserInfo.objects.filter(user_id=author_id).first()
    return render(request, 'v2_front/author/main.html', locals())


def his_blog(request, uid):
    tab_active = "his_blog"
    author_id = int(uid)
    his_blog_list = Article.objects.filter(user__id=author_id, is_check='Yes').order_by("-created_at")
    his_blog_list = paged_items(request, his_blog_list)
    return render(request, 'v2_front/author/blog/his_blog.html', locals())


def his_course(request, uid):
    tab_active = "his_course"
    author_id = int(uid)
    his_book_list = Course.objects.filter(user__id=author_id, status='CheckPass').order_by("-created_at")
    his_book_list = paged_items(request, his_book_list)
    return render(request, 'v2_front/author/course/his_course.html', locals())


def his_video(request, uid):
    tab_active = "his_video"
    author_id = int(uid)
    return render(request, 'v2_front/author/video/his_video.html', locals())
