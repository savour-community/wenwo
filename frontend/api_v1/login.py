#encoding=utf-8

import json
import logging
import base64
import re
from django.shortcuts import render
from django.shortcuts import redirect
from wenwo_auth.models import (
    User,
    UserInfo,
    UserWallet,
    UserWalletRecord
)
from wenwo_auth.helper import (
    send_msg_by_ali,
    get_code,
    hash_code,
    check_api_token,
    check_user_token
)
from django.core.cache import cache
from common.helpers import ok_json, error_json
from django.views.decorators.csrf import csrf_exempt
from common.helpers import dec, d0


@check_api_token
def sms_send(request):
    params = json.loads(request.body.decode())
    phone = params.get('phone', "")
    if phone in [None, ""]:
        return error_json("手机号码错误", 1000)
    else:
        code = get_code(6,  False)
        logging.info("phone is %s code is %s", phone, code)
        cache.set(phone, code, 60)
        if cache.has_key(phone):
            result = send_msg_by_ali(phone, code)
            return ok_json(result)


@check_api_token
def sms_check(request):
    params = json.loads(request.body.decode())
    phone = params.get('phone', "")
    code = params.get('code', "")
    if phone in ["", None] or code in ["", None]:
        return error_json("手机号码或者验证码为空", 1000)
    cache_code = cache.get(phone)
    if code == cache_code:
        return ok_json("ok")
    else:
        return error_json("false", 1000)


@csrf_exempt
@check_api_token
def register(request):
    params = json.loads(request.body.decode())
    phone = params.get('phone', "")
    password = params.get('password', "")
    c_password = params.get('c_password', "")
    v_code = params.get('v_code', "")
    invite_code = params.get('invite_code', "")
    if phone in ["", None]:
        return error_json("手机号码不能为空", 1000)
    user_exist = User.objects.filter(phone=phone).first()
    if user_exist is not None:
        return error_json("该手机号码已被注册", 1000)
    if password in ["", None] or c_password in ["", None]:
        return error_json("密码或者确认密码不能为空", 1000)
    if password != c_password:
        return error_json("密码或者确认密码不相等", 1000)
    if v_code in  ["", None]:
        return error_json("验证码不能为空", 1000)
    if v_code != cache.get(phone):
        return error_json("验证码错误", 1000)
    if invite_code not in ["", None, "None"]:
        user = User.objects.filter(invite_code=invite_code).first()
        invite_user_id = user.id
        user_wallet = UserWallet.objects.filter(
            user=user,
            coin_type="WenwoCoin"
        ).first()
        user_wallet.amount += 100
        user_wallet.save()
        UserWalletRecord.objects.create(
            user=user,
            amount=dec('100'),
            coin_type="WenwoCoin",
            source_type="InviteReward",
            wallet_type="Reward",
        )
    else:
        invite_user_id = 0
    bs = base64.b64encode(phone.encode("utf-8"))
    create_user = User.objects.create(
        user_name="wenwo_user",
        phone=phone,
        token=bs.decode(),
        password=hash_code(password),
        invite_user_id=invite_user_id,
        invite_code=bs.decode()
    )
    UserInfo.objects.create(
        user_id=create_user.id
    )
    UserWallet.objects.create(
        user=create_user,
        coin_type="Cny"
    )
    UserWallet.objects.create(
        user=create_user,
        coin_type="WenwoCoin",
        amount=dec('100')
    )
    UserWallet.objects.create(
        user=create_user,
        coin_type="Cny",
        amount=dec('0')
    )
    UserWalletRecord.objects.create(
        user=create_user,
        amount=dec('100'),
        coin_type="WenwoCoin",
        source_type="Register",
        wallet_type="Reward",
    )
    return ok_json("注册成功")


@check_api_token
def login(request):
    params = json.loads(request.body.decode())
    login_way = params.get('login_way', "password")
    phone = params.get('phone', "")
    password = params.get('password', "")
    v_code = params.get('v_code', "")
    if login_way not in [
        "password", "Password", "PASSWORD",
        "v_code", "Vcode", "VCODE"
    ]:
        return error_json("登陆方式不正确", 1000)
    if phone in ["", None]:
        return error_json("手机号码不能为空", 1000)
    user = User.objects.filter(phone=phone).first()
    if user is None:
        return error_json("该手机号码不存在", 1000)
    if login_way in ["password", "Password", "PASSWORD"]:
        if user.password != hash_code(password):
            return error_json("密码不正确", 1000)
    if login_way in ["v_code", "Vcode", "VCODE"]:
        if v_code != cache.get(phone):
            return error_json("验证码不正确")
    user.login_times = user.login_times + 1
    user.save()
    return ok_json(user.to_dict())


@check_api_token
def forget(request):
    params = json.loads(request.body.decode())
    phone = params.get('phone', "")
    v_code = params.get('v_code', "")
    password = params.get('password', "")
    c_password = params.get('c_password', "")
    if phone in ["", None]:
        return error_json("手机号码不能为空", 1000)
    user = User.objects.filter(phone=phone).first()
    if user is None:
        return error_json("没有这个用户", 1000)
    if password in ["", None] or c_password in ["", None]:
        return error_json("密码或者确认密码不能为空", 1000)
    if password != c_password:
        return error_json("密码或者确认密码不相等", 1000)
    if v_code in ["", None]:
        return error_json("验证码不能为空", 1000)
    if v_code != cache.get(phone):
        return error_json("验证码错误", 1000)
    user.password = hash_code(password)
    return ok_json("找回密码成功")


@check_api_token
@check_user_token
def logout(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("没有这个用户", 1000)
    return ok_json("退出成功")
