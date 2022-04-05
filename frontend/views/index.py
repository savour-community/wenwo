from django.shortcuts import render
from wenwo.models import Banner, Link
from activity.models import Activity
from video_tutorial.models import Video
from topic.models import Topic
from blog.models import Article
from book.models import Course


def global_variable(request):
    link_list = Link.objects.all().order_by('-id')[:100]
    return locals()


def index(request):
    nav_cat = "index"
    type = request.GET.get('type', "blog")
    if type == "question":
        question_list = Topic.objects.all().order_by('-views')[:30]
    elif type == "video":
        video_list = Video.objects.all().order_by('-views')[:30]
    else:
        blog_list = Article.objects.all().order_by('-views')[:30]
    hot_blog_list = Article.objects.all().order_by('-views')[:30]
    hot_course_list = Course.objects.all().order_by('-views')[:30]
    return render(request, 'v2_front/index/index.html', locals())