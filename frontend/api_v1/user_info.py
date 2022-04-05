#encoding=utf-8

import json
from common.helpers import (
    ok_json,
    error_json
)
from wenwo_auth.models import (
    User,
    UserInfo,
    Fans,
    UserWallet,
    UserWalletRecord,
    WithdrawSource
)
from wenwo_auth.helper import check_api_token, check_user_token, hash_code
from topic.models import Topic
from blog.models import Article
from django.core.cache import cache
from common.helpers import dec, d0
from django.core.files.base import ContentFile


@check_api_token
@check_user_token
def get_user_info(request):
    params = json.loads(request.body.decode())
    user_id = params.get('user_id', 0)
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("系统内部没有这个用户")
    return ok_json(user.userif_to_dict())


@check_api_token
@check_user_token
def update_userif(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    user_name = params.get('user_name', "")
    sex = params.get('sex', "")
    introduce = params.get('introduce', "")
    company = params.get('company', "")
    position = params.get('position', "")
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("您还没有登陆", 1000)
    user_info = UserInfo.objects.filter(user_id=user_id).first()
    if user_info is not None:
        user_info.user_sex = sex if sex not in ["", None] else user_info.user_sex
        user_info.user_intro = introduce if introduce not in ["", None] else user_info.user_intro
        user_info.company = company if company not in ["", None] else user_info.company
        user_info.user_pos = position if position not in ["", None] else user_info.user_pos
        user_info.save()
    user.user_name = user_name if user_name not in ["", None] else user.user_name
    user.save()
    return ok_json("修改用户信息成功")


@check_api_token
def update_photo(request):
    user_id = int(request.POST.get("user_id"))
    user_photo = request.FILES.get("user_photo")
    user_info = UserInfo.objects.filter(user_id=user_id).first()
    user_info.user_pho = user_photo
    user_info.save()
    return ok_json("修改头像成功")


@check_api_token
@check_user_token
def update_password(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    old_password = params.get('old_password', None)
    new_password = params.get('new_password', None)
    cnew_password = params.get('cnew_password', None)
    phone = params.get('phone', None)
    v_code = params.get('v_code', None)
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("您还没有登陆", 1000)
    if phone != user.phone:
        return error_json("手机号码不正确", 1000)
    cache_code = cache.get(phone)
    if cache_code != v_code:
        return error_json("手机验证码不正确", 1000)
    if hash_code(old_password) != user.password:
        return error_json("老密码不正确", 1000)
    if new_password != cnew_password:
        return error_json("两次输入的新密码不一样", 1000)
    user.password = hash_code(new_password)
    user.save()
    return ok_json("修改密码成功")


@check_api_token
@check_user_token
def update_phone(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    new_phone = params.get('new_phone', None)
    v_code = params.get('v_code', None)
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("您还没有登陆", 1000)
    cache_code = cache.get(new_phone)
    if cache_code != v_code:
        return error_json("手机验证码不正确", 1000)
    if user.phone == new_phone:
        return error_json("新手机好吗不能和老手机号码一致", 1000)
    user.phone = new_phone
    user.save()
    return ok_json("修改手机号码成功")


@check_api_token
@check_user_token
def my_blog(request):
    params = json.loads(request.body.decode())
    user_id = params.get('user_id', 0)
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    blog_list = Article.objects.filter(user__id=user_id).order_by("-id")[start:end]
    my_blog_return = []
    for blog in blog_list:
        my_blog_return.append(blog.list_to_dict())
    return ok_json(my_blog_return)


@check_api_token
@check_user_token
def my_question(request):
    params = json.loads(request.body.decode())
    user_id = params.get('user_id', 0)
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    topic_list = Topic.objects.filter(user__id=user_id).order_by("-id")[start:end]
    my_tp_return = []
    for tp in topic_list:
        my_tp_return.append(tp.list_to_dict())
    return ok_json(my_tp_return)


@check_api_token
@check_user_token
def focus_other(request):
    params = json.loads(request.body.decode())
    me_user_id = int(params.get('me_user_id', 0))
    focus_user_id = int(params.get('focus_user_id', 0))
    me = User.objects.filter(id=me_user_id).first()
    if me is None:
        return error_json("您还没有登录,请去登录", 1000)
    focus_user = User.objects.filter(id=focus_user_id).first()
    if focus_user is None:
        return error_json("您要关注的人不存在", 1000)
    if me_user_id == focus_user_id:
        return error_json("自己不能关注自己", 1000)
    fans_has = Fans.objects.filter(fans__id=focus_user_id).first()
    if fans_has is not None:
        return error_json("您已经关注过该用户", 1000)
    Fans.objects.create(
        me=me,
        fans=focus_user
    )
    return ok_json("关注成功")


@check_api_token
@check_user_token
def focus_me_list(request):
    params = json.loads(request.body.decode())
    user_id = params.get('user_id', 0)
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("您还没有登录,请去登录", 1000)
    fans_list = Fans.objects.filter(fans=user).order_by("-id")
    fans_return_data = []
    for fans in fans_list:
        fans_return_data.append(fans.focus_me_dict())
    return ok_json(fans_return_data)


@check_api_token
@check_user_token
def my_focus_list(request):
    params = json.loads(request.body.decode())
    user_id = params.get('user_id', 0)
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("您还没有登录,请去登录", 1000)
    fans_list = Fans.objects.filter(me=user).order_by("-id")
    fans_return_data = []
    for fans in fans_list:
        fans_return_data.append(fans.my_focus_dict())
    return ok_json(fans_return_data)


@check_api_token
@check_user_token
def get_my_wallet(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    user_wallet_cny = UserWallet.objects.filter(user__id=user_id, coin_type='Cny').first()
    cny_dec = dec('{:f}'.format(user_wallet_cny.amount)).quantize(dec("0.00"))
    cny_dec_coin = cny_dec.to_integral() if cny_dec == cny_dec.to_integral() else cny_dec.normalize()
    user_wallet_wenwo = UserWallet.objects.filter(user__id=user_id, coin_type='WenwoCoin').first()
    wenwo_coin_dec = dec('{:f}'.format(user_wallet_wenwo.amount)).quantize(dec("0.00"))
    wenwo_coin = wenwo_coin_dec.to_integral() if wenwo_coin_dec == wenwo_coin_dec.to_integral() else wenwo_coin_dec.normalize()
    user_wallet = {
        "cny": cny_dec_coin,
        "wenwo_coin": wenwo_coin,
        "user": user_wallet_cny.to_dict()
    }
    return ok_json(user_wallet)


@check_api_token
@check_user_token
def wallet_record(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    page = int(params.get('page', 0))
    page_size = int(params.get('page_size', 20))
    start = (page - 1) * page_size
    end = start + page_size
    wallet_record_list = UserWalletRecord.objects.filter(user__id=user_id)[start:end]
    record_data_return = []
    for wallet_record in wallet_record_list:
        record_data_return.append(wallet_record.to_dict())
    return ok_json(record_data_return)


@check_api_token
@check_user_token
def create_withdraw_source(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    wd_source = params.get('wd_source', 'WeiChat')
    account = params.get('account', '')
    qr_code = request.FILES.get("qr_code", None)
    user = User.objects.filter(id=user_id).first()
    if user is None:
        return error_json("您还没有登录,请去登录", 1000)
    ws = WithdrawSource.objects.filter(user=user, wd_source=wd_source).first()
    if ws is None:
        WithdrawSource.objects.create(
            user=user,
            wd_source=wd_source,
            account=account,
            qr_code=qr_code,
        )
        return ok_json("提交成功")
    else:
        ws.account = account
        ws.qr_code = qr_code
        ws.save()
        return ok_json("修改成功")


@check_api_token
@check_user_token
def withdraw_source_list(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    wd_source = params.get('wd_source', 'WeiChat')
    ws = WithdrawSource.objects.filter(
        user__id=user_id,
        wd_source=wd_source
    ).first()
    if ws is None:
        return error_json("您还没有提交任何提现相关的账户信息", 1000)
    else:
        return ok_json(ws.to_dict())


@check_api_token
@check_user_token
def withdraw_apply(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    source_id = int(params.get('source_id', 0))
    amount = params.get('amount', d0)
    if source_id in [0, '0']:
        return error_json("提现方式不正确, 请核对后再提交", 1000)
    if amount <= 0:
        return error_json("提现金额应大于 0", 1000)
    user = User.objects.filter(id=user_id).first()
    use_wallet = UserWallet.objects.filter(user__id=user_id, coin_type='Cny').first()
    if use_wallet.amount >= amount:
        UserWalletRecord.objects.create(
            user=user,
            amount=dec(amount),
            coin_type='Cny',
            source_type='Output',
            source_id=source_id,
            wallet_type="Withdraw",
            check_status="Checking",
        )
        return ok_json("提交提现信息成功，提现资金在 3 个工作日之内到账")
    else:
        return error_json("提现失败, 钱包余额不足", 1000)


@check_api_token
@check_user_token
def coin_change(request):
    params = json.loads(request.body.decode())
    user_id = int(params.get('user_id', 0))
    change_way = params.get('change_way', "WenwoCoinToCny")
    if change_way not in ["WenwoCoinToCny", "CnyToWenwoCoin"]:
        return error_json("兑换方式不正确", 1000)
    use_cyn_wallet = UserWallet.objects.filter(user__id=user_id, coin_type='Cny').first()
    user_wwc_wallet = UserWallet.objects.filter(user__id=user_id, coin_type='WenwoCoin').first()
    if change_way == "CnyToWenwoCoin":
        return error_json("暂时不支持该中兑换方式", 1000)
    if change_way == "WenwoCoinToCny":
        if user_wwc_wallet.amount <= 0:
            return error_json("问我积分为 0, 无法发起兑换")
        else:
            use_cyn_wallet.amount = use_cyn_wallet.amount + dec(user_wwc_wallet.amount / 100)
            user_wwc_wallet.amount = 0
            user_wwc_wallet.save()
            use_cyn_wallet.save()
            return ok_json("兑换成功")
