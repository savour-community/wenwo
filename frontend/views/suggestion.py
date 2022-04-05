#encoding=utf-8

import pytz
import logging
import markdown
from django.shortcuts import render
from common.helpers import (
    paged_items,
    ok_json,
    error_json
)
from django.http import JsonResponse
from django.db.models import F
from wenwo.models import Banner
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.shortcuts import redirect
from django.conf import settings
from about.forms.sgt_form import SuggestForm
from wenwo_auth.models import User, UserInfo
from about.models import Suggestion
from frontend.helper import check_user_login

@check_user_login
def my_suggestion(request):
    tab_active = "my_suggestion"
    user_id = request.session.get("user_id")
    sgt_list = Suggestion.objects.filter(user__id=user_id).order_by("-id")
    sgt_list = paged_items(request, sgt_list)
    return render(request, 'v2_front/auth/question/my_suggestion.html', locals())


@check_user_login
def create_sgt(request):
    tab_active = "sgt"
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id).first()
    if request.method == 'GET':
        sgt_form = SuggestForm(request)
        return render(request, 'v2_front/auth/question/create_sgt.html', locals())
    if request.method == 'POST':
        sgt_form = SuggestForm(request, request.POST)
        if sgt_form.is_valid():
            sgt_form.create_suggestion(user)
            return redirect('my_suggestion')
        else:
            error = sgt_form.errors
            return render(
                request, "v2_front/auth/question/create_sgt.html",
                {
                    'sgt_form': sgt_form,
                    'error': error
                }
            )


