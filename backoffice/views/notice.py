#encoding=utf-8


from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from backoffice.helper import check_admin_login
from about.models import Notice
from common.helpers import dec, d0


@check_admin_login
def back_notice_list(request):
    b_notice_list = Notice.objects.all().order_by("-id")
    b_notice_list = paged_items(request, b_notice_list)
    return render(request, 'backend/notice/notice_list.html', locals())


@check_admin_login
def back_notice_detail(request, id):
    b_notice = Notice.objects.filter(id=id).first()
    return render(request, 'backend/notice/notice_detail.html', locals())


