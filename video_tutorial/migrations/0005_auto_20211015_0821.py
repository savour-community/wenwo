# Generated by Django 2.2.7 on 2021-10-15 00:21

import common.model_fields
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wenwo_auth', '0006_userwallet_userwalletrecord'),
        ('video_tutorial', '0004_auto_20211015_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBuyVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wenwo_auth.User', verbose_name='购买人')),
            ],
            options={
                'verbose_name': '用户购买视频表',
                'verbose_name_plural': '用户购买视频表',
            },
        ),
        migrations.DeleteModel(
            name='Contents',
        ),
        migrations.RemoveField(
            model_name='videoreply',
            name='account_id',
        ),
        migrations.RemoveField(
            model_name='videoreply',
            name='video_id',
        ),
        migrations.AddField(
            model_name='charpter',
            name='cmts',
            field=models.PositiveIntegerField(default=0, verbose_name='评论数'),
        ),
        migrations.AddField(
            model_name='charpter',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='查看次数'),
        ),
        migrations.AddField(
            model_name='video',
            name='charpter_num',
            field=models.PositiveIntegerField(default=0, verbose_name='视频章节数量'),
        ),
        migrations.AddField(
            model_name='video',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否是有效'),
        ),
        migrations.AddField(
            model_name='video',
            name='process',
            field=models.CharField(default='0', max_length=100, verbose_name='完成度'),
        ),
        migrations.AddField(
            model_name='videoreply',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wenwo_auth.User', verbose_name='评论用户'),
        ),
        migrations.AddField(
            model_name='videoreply',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='video_tutorial.Video', verbose_name='关联视频'),
        ),
        migrations.AlterField(
            model_name='charpter',
            name='chart',
            field=models.IntegerField(default=0, verbose_name='章节数'),
        ),
        migrations.AlterField(
            model_name='charpter',
            name='chart_name',
            field=models.CharField(default='', max_length=70, verbose_name='章节名称'),
        ),
        migrations.AlterField(
            model_name='charpter',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='video_tutorial.Video', verbose_name='关联视频'),
        ),
        migrations.AlterField(
            model_name='charpter',
            name='video_url',
            field=models.CharField(default='', max_length=70, verbose_name='视频链接'),
        ),
        migrations.AlterField(
            model_name='video',
            name='price',
            field=common.model_fields.DecField(decimal_places=30, default=Decimal('0E-18'), max_digits=65, verbose_name='视频价格'),
        ),
        migrations.AlterField(
            model_name='video',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wenwo_auth.User', verbose_name='发布人'),
        ),
        migrations.AlterField(
            model_name='videoreply',
            name='content',
            field=mdeditor.fields.MDTextField(),
        ),
        migrations.AlterField(
            model_name='videoreply',
            name='like',
            field=models.PositiveIntegerField(default=0, verbose_name='点赞次数'),
        ),
        migrations.AlterField(
            model_name='videoreply',
            name='reply_id',
            field=models.IntegerField(default=0, verbose_name='回复ID'),
        ),
        migrations.AddField(
            model_name='userbuyvideo',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='video_tutorial.Video', verbose_name='关联视频'),
        ),
    ]