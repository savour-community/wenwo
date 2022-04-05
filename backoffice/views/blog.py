#encoding=utf-8

import markdown
from django.shortcuts import redirect, render, reverse
from common.helpers import paged_items
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from blog.models import Article, Category
from backoffice.helper import check_admin_login
from wenwo_auth.models import User, UserWallet, UserWalletRecord
from common.helpers import dec, d0


@check_admin_login
def back_blog_cat_list(request):
    b_cat_list = Category.objects.all().order_by("-id")
    return render(request, 'backend/blog/blog_cat_list.html', locals())


@check_admin_login
def back_blog_list(request):
    title = request.GET.get("title", "")
    b_blog_list = Article.objects.all().order_by("-id")
    if title not in ["", None]:
        b_blog_list = b_blog_list.filter(title__icontains=title)
    b_blog_list = paged_items(request, b_blog_list)
    return render(request, 'backend/blog/blog_list.html', locals())


@check_admin_login
def back_blog_check(request, bid):
    b_blog = Article.objects.filter(id=bid).first()
    b_blog.is_check = "Yes"
    b_blog.is_active = True
    b_blog.save()
    user = User.objects.filter(id=b_blog.user.id).first()
    user_wallet = UserWallet.objects.filter(user=user, coin_type="WenwoCoin").first()
    if user_wallet is not None:
        user_wallet.amount += dec(100)
        user_wallet.save()
        UserWalletRecord.objects.create(
            user=user,
            amount=dec(100),
            coin_type="WenwoCoin",
            source_type="BlogReward",
            source_id=b_blog.id,
            wallet_type="Reward",
            check_status="Checked"
        )
    return redirect('back_blog_list')


@check_admin_login
def back_blog_detail(request, bid):
    title = request.GET.get("title", "")
    b_blog = Article.objects.filter(id=bid).first()
    b_blog.body = markdown.markdown(
        b_blog.body,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    return render(request, 'backend/blog/blog_detail.html', locals())



