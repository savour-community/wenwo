# Generated by Django 2.2.7 on 2021-10-10 22:42

import DjangoUeditor.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200229_1540'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': '文章表', 'verbose_name_plural': '文章表'},
        ),
        migrations.AlterModelOptions(
            name='blogreply',
            options={'verbose_name': '评论回复表', 'verbose_name_plural': '评论回复表'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '类别表', 'verbose_name_plural': '类别表'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '标签表', 'verbose_name_plural': '标签表'},
        ),
        migrations.AlterModelOptions(
            name='tui',
            options={'verbose_name': '推荐表', 'verbose_name_plural': '推荐表'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='account_id',
        ),
        migrations.RemoveField(
            model_name='article',
            name='account_name',
        ),
        migrations.RemoveField(
            model_name='blogreply',
            name='account_id',
        ),
        migrations.RemoveField(
            model_name='blogreply',
            name='account_name',
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=DjangoUeditor.models.UEditorField(blank=True, verbose_name='图片'),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Category', verbose_name='类别'),
        ),
        migrations.AlterField(
            model_name='article',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='article',
            name='excerpt',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='摘要'),
        ),
        migrations.AlterField(
            model_name='article',
            name='like',
            field=models.PositiveIntegerField(default=0, verbose_name='点赞次数'),
        ),
        migrations.AlterField(
            model_name='article',
            name='modified_time',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='blog.Tag', verbose_name='标签'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=70, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tui',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Tui', verbose_name='是否推荐'),
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AlterField(
            model_name='article',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='浏览次数'),
        ),
        migrations.AlterField(
            model_name='blogreply',
            name='blog_id',
            field=models.IntegerField(default=0, verbose_name='博客ID'),
        ),
        migrations.AlterField(
            model_name='blogreply',
            name='content',
            field=models.TextField(default='', max_length=200, verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='blogreply',
            name='like',
            field=models.PositiveIntegerField(default=0, verbose_name='点赞次数'),
        ),
        migrations.AlterField(
            model_name='blogreply',
            name='reply_id',
            field=models.IntegerField(default=0, verbose_name='回复ID'),
        ),
        migrations.AlterField(
            model_name='blogreply',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论人'),
        ),
        migrations.AlterField(
            model_name='category',
            name='index',
            field=models.IntegerField(default=999, verbose_name='分类索引'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='分类名称'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='tui',
            name='name',
            field=models.CharField(max_length=100, verbose_name='名称'),
        ),
    ]
