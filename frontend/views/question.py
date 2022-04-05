#encoding=utf-8

import logging
import markdown
from django.shortcuts import render
from django.shortcuts import redirect
from topic.models import Topic, TopicCategory, TopicReply
from common.helpers import paged_items
from topic.forms.questions_form import TopicForm
from wenwo_auth.models import User, UserInfo
from topic.forms.cmt_forms import TopicReplyForm
from frontend.helper import check_user_login
from wenwo_auth.models import User, UserWallet, UserWalletRecord
from common.helpers import dec, d0


@check_user_login
def create_question(request):
    tab_active = "question"
    user_id = request.session.get("user_id")
    user = User.objects.filter(id=user_id).first()
    if request.method == 'GET':
        topic_form = TopicForm(request)
        return render(request, 'v2_front/auth/question/create_question.html', locals())
    if request.method == 'POST':
        topic_form = TopicForm(request, request.POST)
        if topic_form.is_valid():
            uid = topic_form.create_question(user)
            return redirect('question_list')
        else:
            error = topic_form.errors
            return render(
                request, "v2_front/auth/question/create_question.html",
                {
                    'topic_form': topic_form,
                    'error': error
                }
            )


def question_list(request):
    nav_cat = "question"
    cat_id = request.GET.get("cat_id", 0)
    topic_cat_list = TopicCategory.objects.all()
    if cat_id in [0, '0']:
        topic_list = Topic.objects.filter(is_check='Yes').order_by("-id")
    else:
        topic_list = Topic.objects.filter(is_check='Yes', category__id=cat_id).order_by("-id")
    for topic in topic_list:
        reply_photo_list = []
        t_user_info = UserInfo.objects.filter(user_id=topic.user.id).first()
        if t_user_info is not None:
            topic.user_photo = t_user_info.user_pho
        else:
            topic.user_photo = ""
        topic_reply_list = TopicReply.objects.filter(topic=topic).order_by("-id")
        for topic_reply in topic_reply_list:
            user_info = UserInfo.objects.filter(user_id=topic_reply.user.id).first()
            if user_info is not None:
                reply_photo_list.append(user_info.user_pho)
        topic.reply_photo_list = reply_photo_list
    topic_list = paged_items(request, topic_list)
    return render(request, 'v2_front/question/question_list.html', locals())


def question_detail(request, qid):
    nav_cat = "question"
    user_id = request.session.get("user_id")
    topic = Topic.objects.filter(id=qid).first()
    hot_topic_list = Topic.objects.all().order_by("-views")
    topic_comment_list = TopicReply.objects.filter(topic=topic).order_by("-id")
    for topic_comment in topic_comment_list:
        topic_comment.content = markdown.markdown(
            topic_comment.content,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
    blog_reply_num = len(topic_comment_list)
    topic.views += 1
    topic.save()
    topic.content = markdown.markdown(
        topic.content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    if request.method == 'GET':
        cmt_form = TopicReplyForm(request)
        return render(request, 'v2_front/question/question_detail.html', locals())
    if request.method == 'POST':
        is_login = request.session.get("is_login")
        if is_login:
            cmt_form = TopicReplyForm(request, request.POST)
            if cmt_form.is_valid():
                user = User.objects.filter(id=user_id).first()
                cmt_topic = Topic.objects.get(id=qid)
                cmt_form.create_comment(cmt_topic, 0, user)
                cmt_topic.answers += 1
                cmt_topic.save()
                user_wallet = UserWallet.objects.filter(user=user, coin_type="WenwoCoin").first()
                if user_wallet is not None:
                    user_wallet.amount += dec(20)
                    user_wallet.save()
                    UserWalletRecord.objects.create(
                        user=user,
                        amount=dec(20),
                        coin_type="WenwoCoin",
                        source_type="AnswerReward",
                        source_id=qid,
                        wallet_type="Reward",
                        check_status="Checked"
                    )
                return redirect("question_detail", qid)
            else:
                error = cmt_form.errors
                return render(
                    request,
                    "v2_front/question/question_detail.html",
                    {
                        'cmt_form': cmt_form,
                        'error': error,
                        'topic': topic,
                        'hot_topic_list': hot_topic_list,
                        'topic_comment_list': topic_comment_list,
                        'blog_reply_num': len(topic_comment_list)
                    }
                )
        else:
            return redirect("register")



