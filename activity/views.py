# #encoding=utf-8
#
# import time, datetime
# import logging
# from django.core import serializers
# from django.shortcuts import render
# from activity.models import Activity, ActBanner, Area, ActivityCat
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.shortcuts import reverse,redirect
# from common.helpers import paged_items, ok_json, error_json, parse_int
# from activity.activity_forms import ActivityForm
#
#
# def send_activity(request):
#     if request.method == 'GET':
#         form = ActivityForm()
#         return render(request, 'frontend/wenwo_auth/send_activity.html', locals())
#     elif request.method == 'POST':
#         form = ActivityForm(request.POST)
#         if form.is_valid():
#             title = form.cleaned_data.get('title')
#             category = form.cleaned_data.get('category')
#             position = form.cleaned_data.get('position')
#             tags = form.cleaned_data.get('tags')
#             acttime = form.cleaned_data.get('acttime')
#             excerpt = form.cleaned_data.get('excerpt')
#             company = form.cleaned_data.get('company')
#             author = form.cleaned_data.get('author')
#             actfee = form.cleaned_data.get('actfee')
#             person = form.cleaned_data.get('person')
#             is_help = form.cleaned_data.get('is_help')
#             account_id = request.session.get("user_id")
#             account_name = request.session.get("user_name")
#             img = form.cleaned_data.get('img')
#             content = form.cleaned_data.get('content')
#
#             activity = Activity.objects.create(
#                 title=title,
#                 category=category,
#                 position=position,
#                 acttime=acttime,
#                 excerpt=excerpt,
#                 company=company,
#                 author=author,
#                 actfee=actfee,
#                 person=person,
#                 is_help=is_help,
#                 account_id=account_id,
#                 account_name=account_name,
#                 img=img,
#                 body=content)
#             return redirect('/activity')
#
#         return redirect('/activity')
#
#
# def activity(request):
#     act_banner = ActBanner.objects.filter(is_active=True)[0:6]
#     hot_act = Activity.objects.filter(is_active=True).order_by('views')[:8]
#     actcat = ActivityCat.objects.all()
#     area = Area.objects.all()
#     allarticle = Activity.objects.all().order_by('-id')
#     paginator = Paginator(allarticle, 30)
#     page = request.GET.get('page')
#     try:
#         allarticle = paginator.page(page)
#     except PageNotAnInteger:
#         allarticle = paginator.page(1)
#     except EmptyPage:
#         allarticle = paginator.page(paginator.num_pages)
#     if request.is_ajax():
#         json_data = serializers.serialize("json", allarticle, ensure_ascii=False)
#         return ok_json({'activity': json_data})
#
#     return render(request, 'frontend/activity/activity.html', locals())
#
#
# def activity_list(request,lid):
#     act_list = Activity.objects.filter(category_id=lid)
#     cname = ActivityCat.objects.get(id=lid)
#     page = request.GET.get('page')
#     paginator = Paginator(act_list, 30)
#     try:
#         act_list = paginator.page(page)
#     except PageNotAnInteger:
#         act_list = paginator.page(1)
#     except EmptyPage:
#         act_list = paginator.page(paginator.num_pages)
#     return render(request, 'frontend/activity/activity_list.html', locals())
#
#
# def activity_detail(request,sid):
#     activity_show = Activity.objects.get(id=sid)
#     hot_activity = Activity.objects.all().order_by('?')[:10]
#     previous_blog = Activity.objects.filter(created_time__gt=activity_show.created_time,category=activity_show.category.id).first()
#     netx_blog = Activity.objects.filter(created_time__lt=activity_show.created_time,category=activity_show.category.id).last()
#     activity_show.views = activity_show.views + 1
#     activity_show.save()
#     return render(request, 'frontend/activity/activity_detail.html', locals())
#
#
# def activity_tag(request, tag):
#     act_list = Activity.objects.filter(tags__name=tag)
#     tname = Area.objects.get(name=tag)
#     page = request.GET.get('page')
#     paginator = Paginator(act_list, 30)
#     try:
#         act_list = paginator.page(page)
#     except PageNotAnInteger:
#         act_list = paginator.page(1)
#     except EmptyPage:
#         act_list = paginator.page(paginator.num_pages)
#     return render(request, 'frontend/activity/activity_tag.html', locals())
#
#
#
