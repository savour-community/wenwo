#encoding=utf-8

import random
import hashlib
import json
import logging
from django.http import HttpRequest
from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from django.core.cache import cache
from wenwo_auth.models import User, ApiAuth
from common.helpers import ok_json, error_json


# 阿里发送短信验证码
def send_msg_by_ali(phone_numbers: str, code: str):
    client = AcsClient(settings.ACCESSKEYID,
                       settings.ACCESSSECRET,
                       'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('http')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone_numbers)
    request.add_query_param('SignName', settings.SIGNNAME)
    request.add_query_param('TemplateCode', settings.TEMPLATECODE)
    request.add_query_param('TemplateParam', {"code": code})

    response = client.do_action(request)
    result = (str(response, encoding='utf-8'))
    return result


def get_code(number=6, alpha=False):
    verify_code = ''
    for i in range(number):
        num = random.randint(0, 9)
        if alpha is True:
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            num = random.choice([num, upper_alpha, lower_alpha])
        verify_code = verify_code + str(num)
    return verify_code


def hash_code(s, salt='mysite_login'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


def check_user_token(func):
    def user_auth(request, *args, ** kwargs):
        auth_token = request.META.get("HTTP_AUTH_TOKEN")
        logging.info("auth_token=%s", auth_token)
        user = User.objects.filter(token=auth_token).first()
        if user is None:
            return error_json("您还没有登陆，请去登陆", 1001)
        if user.token_is_expire == 'EXPIRED' :
            return error_json("您的登陆信息已经过期，请重新登陆", 1001)
        return func(request, *args, **kwargs)
    return user_auth


def check_api_token(func):
    def api_auth(request, *args, ** kwargs):
        api_token = request.META.get("HTTP_API_TOKEN")
        logging.info("api_token=%s ", api_token)
        if api_token in ["", "None", None, "unkown"]:
            return error_json("Api Token 为空", 1000)
        api_auth = ApiAuth.objects.filter(api_token=api_token).first()
        if api_auth is None:
            return error_json("Api Token 不存在", 1000)
        if api_auth.status in ['UnVerify', 'Verifing']:
            return error_json("Api Token 审核中", 1000)
        if api_auth.is_expire == "YES":
            return error_json("Api Token 已经过期", 1000)
        return func(request, *args, **kwargs)
    return api_auth



