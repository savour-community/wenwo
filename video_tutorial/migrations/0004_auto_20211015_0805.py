# Generated by Django 2.2.7 on 2021-10-15 00:05

import common.model_fields
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('video_tutorial', '0003_video_account_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Direction',
        ),
        migrations.RemoveField(
            model_name='charpter',
            name='video_id',
        ),
        migrations.RemoveField(
            model_name='video',
            name='account_id',
        ),
        migrations.RemoveField(
            model_name='video',
            name='account_name',
        ),
        migrations.AddField(
            model_name='charpter',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='video_tutorial.Video'),
        ),
        migrations.AddField(
            model_name='charpter',
            name='video_url',
            field=models.CharField(default='', max_length=70),
        ),
        migrations.AddField(
            model_name='video',
            name='buyers',
            field=models.PositiveIntegerField(default=0, verbose_name='购买人数'),
        ),
        migrations.AddField(
            model_name='video',
            name='cmts',
            field=models.PositiveIntegerField(default=0, verbose_name='评论数'),
        ),
        migrations.AddField(
            model_name='video',
            name='price',
            field=common.model_fields.DecField(decimal_places=30, default=Decimal('0E-18'), max_digits=65),
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='video_tutorial.VideoCategory', verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='video',
            name='excerpt',
            field=models.TextField(blank=True, max_length=200, verbose_name='摘要'),
        ),
        migrations.AlterField(
            model_name='video',
            name='like',
            field=models.PositiveIntegerField(default=0, verbose_name='点赞次数'),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=70, verbose_name='标题'),
        ),
        migrations.AlterField(
            model_name='video',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wenwo_auth.User', verbose_name='发布人'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_img',
            field=models.ImageField(blank=True, null=True, upload_to='video_img/%Y/%m/%d/', verbose_name='视频图片'),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_intro',
            field=mdeditor.fields.MDTextField(),
        ),
        migrations.AlterField(
            model_name='video',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='查看次数'),
        ),
        migrations.AlterField(
            model_name='videocategory',
            name='index',
            field=models.IntegerField(default=999, verbose_name='分类索引'),
        ),
        migrations.AlterField(
            model_name='videocategory',
            name='name',
            field=models.CharField(max_length=100, verbose_name='分类名称'),
        ),
    ]
