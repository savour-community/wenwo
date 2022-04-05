#encoding=utf-8

from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from wenwo_auth.models import (
    User,
    UserInfo,
    Account,
    UserWallet,
    UserWalletRecord
)
from backoffice.forms.login_form import AccountLoginForm
from backoffice.helper import check_admin_login


def backend_login(request):
    if request.method == "GET":
        login_form = AccountLoginForm(request)
        return render(request, "backend/user/login.html", locals())
    elif request.method == "POST":
        login_form = AccountLoginForm(request, request.POST)
        if login_form.is_valid():
            user_name = login_form.clean_user_name()
            user = Account.objects.filter(name=user_name).first()
            request.session["backend_is_login"] = True
            request.session["b_user_id"] = user.id
            request.session["b_user_name"] = user.name
            request.session["b_role"] = user.role
            user.online = "Yes"
            user.save()
            return redirect("back_blog_list")
        else:
            error = login_form.errors
            return render(
                request, 'backend/user/login.html',
                {'login_form': login_form, 'error': error}
            )


@check_admin_login
def backend_logout(request):
    request.session["backend_is_login"] = False
    request.session.flush()
    return redirect("backend_login")


@check_admin_login
def back_user_list(request):
    user_name = request.GET.get("user_name", "")
    b_user_list = User.objects.all().order_by("-id")
    if user_name not in ["", None]:
        b_user_list = b_user_list.filter(user_name=user_name)
    b_user_list = paged_items(request, b_user_list)
    return render(request, 'backend/user/user_list.html', locals())


@check_admin_login
def back_user_detail(request, uid):
    b_user = User.objects.filter(id=uid).first()
    b_user_info = UserInfo.objects.filter(user_id=uid).first()
    return render(request, 'backend/user/user_detail.html', locals())


@check_admin_login
def back_user_wallet(request):
    uw_list = UserWallet.objects.filter(is_del='No').order_by('-id')
    b_uw_list = paged_items(request, uw_list)
    return render(request, 'backend/user/user_wallet.html', locals())


@check_admin_login
def back_uw_record(request, uid):
    uw_record_list = UserWalletRecord.objects.filter(user__id=uid).order_by('-id')
    b_uw_record_list = paged_items(request, uw_record_list)
    return render(request, 'backend/user/user_wallet_record.html', locals())




