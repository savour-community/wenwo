#encoding=utf-8

import logging
import markdown
from django.shortcuts import render
from django.shortcuts import redirect
from video_tutorial.models import (
    VideoCategory,
    Video,
    VideoReply,
    UserBuyVideo,
    Charpter
)
from common.helpers import paged_items
from video_tutorial.forms.cmt_forms import VideoReplyForm
from wenwo_auth.models import User, UserInfo
from django.views.decorators.csrf import csrf_exempt
from video_tutorial.forms.video_froms import VideoForm
from video_tutorial.forms.video_charpter_froms import CharpterForm
from frontend.helper import check_user_login


def video_list(request):
    nav_cat = "video"
    cat_id = int(request.GET.get("cat_id", 0))
    level = request.GET.get("level", "all")
    order_by = request.GET.get("order_by", "latest")
    v_cat_list = VideoCategory.objects.filter(is_active=True)
    video_list = Video.objects.filter(is_active=True).order_by("-id")
    if cat_id not in ["0", "", 0]:
        category = VideoCategory.objects.filter(id=cat_id).first()
        video_list = video_list.filter(category=category)
    if level not in ["all", ""]:
        video_list = video_list.filter(level=level)
    if order_by == "latest":
        video_list = video_list.order_by("-created_at")
    if order_by == "number":
        video_list = video_list.order_by("-views")
    video_list = paged_items(request, video_list)
    return render(request, 'v2_front/video/video_list.html', locals())


def video_detail(request, vid):
    nav_cat = "video"
    tab_v = request.GET.get("tab_v", "introduce")
    video_dtl = Video.objects.filter(id=vid).first()
    video_dtl.views += 1
    video_dtl.save()
    video_dtl.video_intro = markdown.markdown(
        video_dtl.video_intro,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    user_info = UserInfo.objects.filter(user_id=video_dtl.user.id).first()
    user_list = UserBuyVideo.objects.filter(video=video_dtl).order_by("-id")
    user_course_list = Video.objects.filter(user=video_dtl.user).order_by("-id")
    vr_list = VideoReply.objects.filter(video=video_dtl).order_by("-id")
    video_total = len(user_course_list)
    video_chapters = Charpter.objects.filter(video=video_dtl)
    return render(request, 'v2_front/video/video_detail.html', locals())


def video_chapter(request, vid):
    nav_cat = "video"
    user_id = request.session.get("user_id")
    cid = int(request.GET.get('cid', 0))
    video_dtl = Video.objects.filter(id=vid).first()
    video_dtl.views += 1
    video_dtl.save()
    video_chapters = Charpter.objects.filter(video=video_dtl).order_by('id')
    if cid in [0, '0']:
        vc_dtl = video_chapters.first()
        cid = vc_dtl.id
    else:
        vc_dtl = Charpter.objects.get(id=cid)
    vc_dtl.views += 1
    vc_dtl.save()
    user_course_list = Video.objects.filter(user=video_dtl.user).order_by("-id")
    video_total = len(user_course_list)
    if request.method == 'GET':
        cmt_form = VideoReplyForm(request)
        return render(request, 'v2_front/video/video_chapter.html', locals())
    if request.method == 'POST':
        is_login = request.session.get("is_login")
        if is_login:
            cmt_form = VideoReplyForm(request, request.POST)
            if cmt_form.is_valid():
                user = User.objects.filter(id=user_id).first()
                video_dtl_cmt = Video.objects.get(id=vid)
                cmt_form.create_comment(video_dtl_cmt, 0, user)
                video_dtl_cmt.cmts += 1
                video_dtl_cmt.save()
                return redirect("blog_detail", sid)
            else:
                error = cmt_form.errors
                return render(
                    request,
                    "v2_front/video/video_chapter.html",
                    {
                        'cmt_form': cmt_form,
                        'error': error,
                        'show': show,
                        'hot_list': hot_list,
                        'tag_name_lists': tag_name_lists,
                        'blog_comment_list': blog_comment_list,
                        'blog_reply_num': len(blog_comment_list)
                    }
                )
        else:
            return redirect("register")



@csrf_exempt
@check_user_login
def create_video(request):
    nav_cat = "video"
    tab_active = "my_video"
    user_id = request.session.get("user_id")
    if request.method == "GET":
        video_form = VideoForm(request)
        return render(request, "v2_front/auth/video/create_video.html", locals())
    if request.method == "POST":
        video_form = VideoForm(request, request.POST, request.FILES)
        if video_form.is_valid():
            user = User.objects.filter(id=user_id).first()
            video_form.create_video(user)
            return redirect('my_video')
        else:
            error = video_form.errors
            return render(
                request, "v2_front/auth/video/create_video.html",
                {
                    'user_id': int(uid),
                    'video_form': video_form,
                    'error': error
                }
            )


@csrf_exempt
@check_user_login
def update_video(request, vid):
    nav_cat = "video"
    tab_active = "my_video"
    video = Video.objects.filter(id=vid).first()
    uid = request.session.get("user_id")
    if request.method == "GET":
        video_form = VideoForm(request, instance=video)
        return render(request, "v2_front/auth/video/update_video.html", locals())
    if request.method == "POST":
        video_form = VideoForm(request, request.POST, request.FILES, instance=video)
        if video_form.is_valid():
            uid = video_form.update_video(video.id)
            return redirect('my_video')
        else:
            error = video_form.errors
            return render(
                request, "v2_front/auth/video/update_video.html",
                {
                    "user_id": uid,
                    "video": video,
                    'video_form': video_form,
                    'error': error
                }
            )


@csrf_exempt
@check_user_login
def create_video_chapter(request, vid):
    nav_cat = "video"
    tab_active = "my_video"
    video = Video.objects.filter(id=vid).first()
    video_id = int(vid)
    v_chapter_list = Charpter.objects.filter(video__id=vid)
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id).first()
    if request.method == "GET":
        chapter_form = CharpterForm(request)
        return render(request, "v2_front/auth/video/create_video_chapter.html", locals())
    if request.method == "POST":
        chapter_form = CharpterForm(request, request.POST, request.FILES)
        if chapter_form.is_valid():
            Charpter.objects.create(
                video=video,
                status="Checking",
                chart=chapter_form.clean_chart(),
                chart_name=chapter_form.clean_chart_name(),
                video_url=chapter_form.clean_video_url(),
                time_long="10.00"
            )
            return redirect('create_video_chapter', int(vid))
        else:
            error = chapter_form.errors
            return render(
                request, "v2_front/auth/video/create_video_chapter.html",
                {
                    "v_chapter_list": v_chapter_list,
                    "user": user,
                    "video_id": video_id,
                    'user_id': user_id,
                    'chapter_form': chapter_form,
                    'error': error
                }
            )