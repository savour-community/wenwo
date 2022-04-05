#encoding=utf-8

import markdown
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from video_tutorial.models import Video, VideoCategory, Charpter
from backoffice.helper import check_admin_login


@check_admin_login
def back_video_cat_list(request):
    b_cat_list = VideoCategory.objects.all().order_by("-id")
    return render(request, 'backend/blog/blog_cat_list.html', locals())


@check_admin_login
def back_vedio_list(request):
    vedio_list = Video.objects.filter(is_active=True).order_by("-id")
    vedio_list = paged_items(request, vedio_list)
    return render(request, 'backend/video/back_vedio_list.html', locals())


@check_admin_login
def back_vedio_check(request, vid):
    status = request.GET.get("status", "CheckPass")
    vedio = Video.objects.filter(id=vid).first()
    if status == "CheckFail":
        vedio.check_reason = \
            "请检查文章格式是否正确，内容是否包含广告和内容是否触犯国家法律法规"
    vedio.status = status
    vedio.is_active = True
    vedio.save()
    return redirect('back_vedio_list')


@check_admin_login
def back_vedio_detail(request, vid):
    vedio_dtl = Video.objects.filter(id=vid).first()
    return render(request, 'backend/video/back_vedio_detail.html', locals())


@check_admin_login
def back_vedio_chapter(request, cid):
    chapter_list = Charpter.objects.filter(is_active=True).order_by("-id")
    chapter_list = paged_items(request, chapter_list)
    return render(request, 'backend/video/back_vedio_chapter.html', locals())


@check_admin_login
def bv_chapter_checked(request, vid):
    status = request.GET.get("status", "CheckPass")
    chapter_detail = Charpter.objects.filter(id=vid).first()
    if status == "CheckFail":
        chapter_detail.check_reason = \
            "请检查文章格式是否正确，内容是否包含广告和内容是否触犯国家法律法规"
    chapter_detail.status = status
    chapter_detail.is_active = True
    chapter_detail.save()
    return redirect('back_vedio_chapter', chapter_detail.video.id)
