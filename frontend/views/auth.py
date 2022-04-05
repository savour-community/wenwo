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
from wenwo_auth.forms.login_form import (
    UserPwdLoginForm,
    UserCodeLoginForm
)
from wenwo_auth.forms.regist_form import UserRegisterForm
from wenwo_auth.forms.forget_form import ForgetPasswordForm
from wenwo_auth.helper import (
    send_msg_by_ali,
    get_code,
    hash_code
)
from django.core.cache import cache
from common.helpers import ok_json, error_json, paged_items
from django.views.decorators.csrf import csrf_exempt
from blog.models import Article
from topic.models import Topic
from book.models import Course, CourseArtcle
from video_tutorial.models import Video, Charpter
from frontend.helper import check_user_login


# 发送短信验证码
def sms_send(request):
    phone = request.GET.get('phone')
    code = get_code(6,  False)
    logging.info("phone is %s code is %s", phone, code)
    cache.set(phone, code, 60)
    if cache.has_key(phone):
        result = send_msg_by_ali(phone, code)
        return ok_json(result)


# 短信验证码校验
def sms_check(request):
    phone = request.GET.get('phone')
    code = request.GET.get('code')
    cache_code = cache.get(phone)
    if code == cache_code:
        return ok_json("ok")
    else:
        return error_json("False")


def register(request):
    if request.method == "GET":
        register_form = UserRegisterForm(request)
        return render(request, 'v2_front/auth/register.html', locals())
    if request.method == "POST":
        register_form = UserRegisterForm(request, request.POST)
        if register_form.is_valid():
            register_form.save_register_user()
            return redirect("login")
        else:
            error = register_form.errors
            return render(
                request,
                'v2_front/auth/register.html',
                {
                    'register_form': register_form,
                    'error': error
                }
            )


def login(request):
    login_way = request.GET.get("login_way", "password")
    if request.session.get("is_login", None):
        return redirect("index")
    if request.method == "GET":
        if login_way == "password":
            login_form = UserPwdLoginForm(request)
        if login_way == "verify":
            login_form = UserCodeLoginForm(request)
        return render(request, 'v2_front/auth/login.html', locals())
    if request.method == "POST":
        if login_way == "password":
            login_form = UserPwdLoginForm(request, request.POST)
            if login_form.is_valid():
                user = User.objects.filter(phone=login_form.clean_phone()).first()
                user_info = UserInfo.objects.filter(user_id=user.id).first()
                request.session["is_login"] = True
                request.session["user_id"] = user.id
                request.session["user_name"] = user.user_name
                request.session["user_pho"] = user_info.user_pho
                user.login_times = user.login_times + 1
                user.save()
                return redirect("index")
            else:
                error = login_form.errors
                return render(
                    request,
                    'v2_front/auth/login.html',
                    {
                        'login_form': login_form,
                        'error': error,
                        'login_way': "password"
                    }
                )
        if login_way == "verify":
            login_form = UserCodeLoginForm(request, request.POST)
            if login_form.is_valid():
                user = User.objects.filter(phone=login_form.clean_phone()).first()
                user_info = UserInfo.objects.filter(user_id=user.id).first()
                request.session["is_login"] = True
                request.session["user_id"] = user.id
                request.session["user_name"] = user.user_name
                request.session["user_pho"] = user_info.user_pho
                user.login_times = user.login_times + 1
                user.save()
                return redirect("index")
            else:
                error = login_form.errors
                return render(
                    request,
                    'v2_front/auth/login.html',
                    {
                        'login_form': login_form,
                        'error': error,
                        'login_way': "verify",
                    }
                )


def forget(request):
    if request.method == "GET":
        forget_form = ForgetPasswordForm(request)
        return render(request, 'v2_front/auth/forget_pwd.html', locals())
    if request.method == "POST":
        forget_form = ForgetPasswordForm(request, request.POST)
        if forget_form.is_valid():
            user = User.objects.filter(phone=forget_form.clean_phone()).first()
            forget_form.update_password(user)
            return redirect("login")
        else:
            error = forget_form.errors
            return render(
                request,
                "v2_front/auth/forget_pwd.html",
                {'forget_form': forget_form, 'error': error}
            )


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/')
    request.session.flush()
    return redirect('/')


@check_user_login
def person_info(request):
    tab_active = "person_info"
    uid = request.session.get('user_id')
    user = User.objects.filter(id=uid).first()
    user_info = UserInfo.objects.filter(user_id=uid).first()
    return render(request, 'v2_front/auth/personal/personal_info.html', locals())


@csrf_exempt
@check_user_login
def update_user_info(request, uid):
    user_id = request.POST.get("user_id")
    user_name = request.POST.get("user_name")
    user_company = request.POST.get("user_company", "")
    user_position = request.POST.get("user_position", "")
    user_photo = request.FILES.get('user_photo')
    user_sex = request.POST.get("user_sex", "")
    user_introduce = request.POST.get("user_introduce", "")
    user = User.objects.filter(id=user_id).order_by("-id").first()
    if user is not None:
        user.user_name = user_name
        user.save()
        user_info = UserInfo.objects.filter(user_id=user_id).order_by("-id").first()
        if user_info is not None:
            user_info.user_sex = user_sex
            user_info.user_intro = user_introduce
            user_info.company = user_company
            user_info.user_pos = user_position
            user_info.user_pho = user_photo
            user_info.save()
    return redirect('person_info')


@check_user_login
def focus_other_web(request, fid):
    user_id = request.session.get('user_id')
    focus_user_id = int(fid)
    me = User.objects.filter(id=user_id).first()
    focus_user = User.objects.filter(id=focus_user_id).first()
    if user_id == focus_user_id:
        return redirect('my_focus_web')
    fans_has = Fans.objects.filter(fans__id=focus_user_id).first()
    if fans_has is not None:
        return redirect('my_focus_web')
    if me is not None and focus_user is not None:
        Fans.objects.create(
            me=me,
            fans=focus_user
        )
    return redirect('my_focus_web')


@check_user_login
def focus_me_web(request):
    tab_active = "focus_me_web"
    user_id = request.session.get('user_id')
    user = User.objects.filter(id=user_id).first()
    fans_list = Fans.objects.filter(fans=user).order_by("-id")
    for fan in fans_list:
        user_info = UserInfo.objects.filter(user_id=fan.me.id).first()
        if user_info is not None:
            fan.user_pho = user_info.user_pho
            fan.user_pos = user_info.user_pos
    fans_list = paged_items(request, fans_list)
    return render(request, 'v2_front/auth/focus/focus_me.html', locals())


@check_user_login
def my_focus_web(request):
    tab_active = "my_focus_web"
    user_id = request.session.get('user_id')
    user = User.objects.filter(id=user_id).first()
    fans_list = Fans.objects.filter(me=user).order_by("-id")
    for fan in fans_list:
        user_info = UserInfo.objects.filter(user_id=fan.fans.id).first()
        if user_info is not None:
            fan.user_pho = user_info.user_pho
            fan.user_pos = user_info.user_pos
    fans_list = paged_items(request, fans_list)
    return render(request, 'v2_front/auth/focus/my_focus.html', locals())


@check_user_login
def my_blog(request):
    tab_active = "my_blog"
    uid = request.session.get('user_id')
    blog_list = Article.objects.filter(user__id=uid).order_by("-id")
    blog_list = paged_items(request, blog_list)
    return render(request, 'v2_front/auth/blog/my_blog.html', locals())


@check_user_login
def my_question(request):
    tab_active = "my_question"
    uid = request.session.get('user_id')
    topic_list = Topic.objects.filter(user__id=uid).order_by("-id")
    topic_list = paged_items(request, topic_list)
    return render(request, 'v2_front/auth/question/my_qusetion.html', locals())


@check_user_login
def my_wallet(request):
    tab_active = "my_wallet"
    top_active = "my_wallet"
    uid = request.session.get('user_id')
    cny_user_wallet = UserWallet.objects.filter(user__id=uid, coin_type="Cny").first()
    wenwo_user_wallet = UserWallet.objects.filter(user__id=uid, coin_type="WenwoCoin").first()
    wallet_record_list = UserWalletRecord.objects.filter(user__id=uid).order_by("-id")
    return render(request, 'v2_front/auth/wallet/my_wallet.html', locals())


@check_user_login
def withdraw_wallet(request):
    tab_active = "my_wallet"
    top_active = "withdraw_wallet"
    uid = request.session.get('user_id')
    user_wallet = UserWallet.objects.filter(user__id=uid).first()
    return render(request, 'v2_front/auth/wallet/withdraw_wallet.html', locals())


@check_user_login
def my_course(request):
    tab_active = "my_course"
    top_active = "my_course"
    pay_way = request.POST.get("pay_way")
    course_name = request.GET.get("course_name", "")
    uid = request.session.get('user_id')
    total_course = Course.objects.filter(user__id=uid).count()
    total_active_course = Course.objects.filter(user__id=uid, is_active=True).count()
    total_unactive_course = Course.objects.filter(user__id=uid, is_active=False).count()
    total_checking_course = Course.objects.filter(user__id=uid, status="Checking").count()
    course_list = Course.objects.filter(user__id=uid).order_by('-id')
    if course_name not in ["", None]:
        course_list = course_list.filter(title__icontains=course_name)
    if pay_way == "free":
        course_list = course_list.filter(price=0)
    if pay_way == "unfree":
        course_list = course_list.filter(price__gt=0)
    course_list = paged_items(request, course_list)
    return render(request, 'v2_front/auth/course/my_course.html', locals())


@check_user_login
def my_video(request):
    tab_active = "my_video"
    top_active = "my_video"
    pay_way = request.POST.get("pay_way")
    course_name = request.GET.get("course_name", "")
    uid = request.session.get('user_id')
    total_course = Video.objects.filter(user__id=uid).count()
    total_active_course = Video.objects.filter(user__id=uid, is_active=True).count()
    total_unactive_course = Video.objects.filter(user__id=uid, is_active=False).count()
    total_checking_course = Video.objects.filter(user__id=uid, status="Checking").count()
    course_list = Video.objects.filter(user__id=uid).order_by('-id')
    if course_name not in ["", None]:
        course_list = course_list.filter(title__icontains=course_name)
    if pay_way == "free":
        course_list = course_list.filter(price=0)
    if pay_way == "unfree":
        course_list = course_list.filter(price__gt=0)
    course_list = paged_items(request, course_list)
    return render(request, 'v2_front/auth/video/my_video.html', locals())
