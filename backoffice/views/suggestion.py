#encoding=utf-8

import markdown
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from topic.models import Topic
from backoffice.helper import check_admin_login
from about.models import Suggestion
from common.helpers import dec, d0
from wenwo_auth.models import User, UserWallet, UserWalletRecord


@check_admin_login
def back_suggestion_list(request):
    b_suggestion_list = Suggestion.objects.all().order_by("-id")
    b_suggestion_list = paged_items(request, b_suggestion_list)
    return render(request, 'backend/question/suggestion_list.html', locals())


@check_admin_login
def back_suggestion_detail(request, id):
    b_suggestion = Suggestion.objects.filter(id=id).first()
    return render(request, 'backend/question/suggestion_detail.html', locals())


@check_admin_login
def accpet_suggestion(request, id):
    accpet = request.GET.get("accpet", 'Accept')
    sg = Suggestion.objects.filter(id=id).first()
    if accpet == 'Accept':
        user = User.objects.filter(id=sg.user.id).first()
        user_wallet = UserWallet.objects.filter(user=user, coin_type="WenwoCoin").first()
        if user_wallet is not None:
            user_wallet.amount += dec(200)
            user_wallet.save()
            UserWalletRecord.objects.create(
                user=user,
                amount=dec(200),
                coin_type="WenwoCoin",
                source_type="FeedBackReward",
                source_id=sg.id,
                wallet_type="Reward",
                check_status="Checked"
            )
        sg.status = 'Accept'
        sg.save()
    else:
        sg.status = 'Refuse'
        sg.save()
    return redirect('back_suggestion_list')

