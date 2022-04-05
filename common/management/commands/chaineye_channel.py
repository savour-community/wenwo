#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from common.rest_client import RestClient
from django.conf import settings
from blog.models import Article, Category
from book.models import Course, CourseArtcle, CourseCat
from wenwo_auth.models import User


BlogUrl = "http://127.0.0.1:19016/backoffice/get_blogs"
ChainSafeUrl = "http://127.0.0.1:19016/backoffice/get_chainsafe"
CourseUrl = "http://127.0.0.1:19016/backoffice/get_course"
RequestPageData = {"page": 0, "page_size": 2000}
BearerHeader = { "Authorization": "Bearer {}".format(settings.API_TOKEN) }


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.sync_article()
        self.sync_chainsafe()
        # self.sync_course()

    def sync_article(self):
        rc = RestClient()
        result = rc.api_post(url=BlogUrl, data=json.dumps(RequestPageData), headers=BearerHeader)
        if result["ok"] is True:
            blog_list = result["result"]
            for blog in blog_list:
                article = Article.objects.filter(title=blog['title']).first()
                if article is None:
                    Article.objects.create(
                        title=blog["title"],
                        excerpt=blog["excerpt"],
                        category=Category.objects.filter(name="区块链").first(),
                        body=blog["body"],
                        user=User.objects.filter(id=34).first(),
                        is_check="Yes",
                        is_active=True
                    )

    def sync_chainsafe(self):
        rc = RestClient()
        result = rc.api_post(url=ChainSafeUrl, data=json.dumps(RequestPageData), headers=BearerHeader)
        if result["ok"] is True:
            blog_list = result["result"]
            for blog in blog_list:
                article = Article.objects.filter(title=blog['title']).first()
                if article is None:
                    Article.objects.create(
                        title=blog["title"],
                        excerpt=blog["excerpt"],
                        category=Category.objects.filter(name="区块链").first(),
                        body=blog["body"],
                        user=User.objects.filter(id=34).first(),
                        is_check="Yes",
                        is_active=True
                    )

    def sync_course(self):
        rc = RestClient()
        result = rc.api_post(url=CourseUrl, data=json.dumps(RequestPageData), headers=BearerHeader)
        if result["ok"] is True:
            course_list = result["result"]
            for course in course_list:
                article = course["article"]
                cse = Course.objects.filter(title=article["title"]).first()
                if cse is None:
                    cse = Course.objects.create(
                        title=article["title"],
                        logo=article["logo"],
                        excerpt=article["excerpt"],
                        category=CourseCat.objects.filter(name="区块链").first(),
                        detail=article["detail"],
                        price=article["price"],
                        status="CheckPass",
                        article_num=article["article_num"],
                        process=article["process"]
                    )
                course_article_list = course["course_article"]
                for course_article in course_article_list:
                    CourseArtcle.objects.create(
                        part=course_article["part"],
                        title=course_article["title"],
                        course=cse,
                        detail=course_article["detail"],
                        status="CheckPass",
                        is_active =True
                    )
