#encoding=utf-8

import pytz
import json
import logging
from common.helpers import (
    ok_json,
    error_json
)
from common.models import Helper, Version
from wenwo_auth.helper import check_api_token


@check_api_token
def help_list(request):
    params = json.loads(request.body.decode())
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    help_list = Helper.objects.filter(is_active=True).order_by("-id")[start:end]
    help_return_data = []
    for help in help_list:
        help_return_data.append(help.to_dict())
    return ok_json(help_return_data)


@check_api_token
def help_detail(request):
    params = json.loads(request.body.decode())
    help_id = int(params.get('help_id', 0))
    helper = Helper.objects.filter(id=help_id).first()
    if helper is not None:
        helper_data = {
            'id': helper.id,
            'title': helper.title,
            'detail': helper.detail,
        }
        return ok_json(helper_data)
    else:
        return error_json("该帮助信息不存在", 1000)


@check_api_token
def version_info(request):
    params = json.loads(request.body.decode())
    platform = params.get('platform', 0)
    version = Version.objects.filter(platforms=platform).first()
    if version is not None:
        return ok_json(version.to_dict())
    else:
        return error_json("该平台不存在", 1000)

