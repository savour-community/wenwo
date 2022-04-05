#encoding=utf-8

import markdown
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from topic.models import Topic, TopicCategory
from backoffice.helper import check_admin_login
from wenwo_auth.models import User, UserWallet, UserWalletRecord
from common.helpers import dec, d0


@check_admin_login
def back_topic_cat_list(request):
    b_cat_list = TopicCategory.objects.all().order_by("-id")
    return render(request, 'backend/blog/blog_cat_list.html', locals())


@check_admin_login
def back_question_list(request):
    title = request.GET.get("title", "")
    b_topic_list = Topic.objects.all().order_by("-id")
    if title not in ["", None]:
        b_topic_list = b_topic_list.filter(title__icontains=title)
    back_topic_list = paged_items(request, b_topic_list)
    return render(request, 'backend/question/question_list.html', locals())


@check_admin_login
def back_question_check(request, tid):
    b_topic = Topic.objects.filter(id=tid).first()
    b_topic.is_check = "Yes"
    b_topic.save()
    user = User.objects.filter(id=b_topic.user.id).first()
    user_wallet = UserWallet.objects.filter(user=user, coin_type="WenwoCoin").first()
    if user_wallet is not None:
        user_wallet.amount += dec(10)
        user_wallet.save()
        UserWalletRecord.objects.create(
            user=user,
            amount=dec(10),
            coin_type="WenwoCoin",
            source_type="QuestionReward",
            source_id=b_topic.id,
            wallet_type="Reward",
            check_status="Checked"
        )
    return redirect('back_question_list')


@check_admin_login
def back_question_detail(request, tid):
    b_topic = Topic.objects.filter(id=tid).first()
    b_topic.content = markdown.markdown(
        b_topic.content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    return render(request, 'backend/question/question_detail.html', locals())
