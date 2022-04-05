# Generated by Django 2.2.7 on 2021-10-21 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wenwo_auth', '0008_auto_20211021_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwalletrecord',
            name='source_type',
            field=models.CharField(choices=[('WeiChat', 'WeiChat'), ('ZhiFuBao', 'ZhiFuBao'), ('InviteReward', 'InviteReward'), ('Register', 'Register'), ('BlogReward', 'BlogReward'), ('CourseReward', 'CourseReward'), ('VideoReward', 'VideoReward')], default='Register', max_length=16, verbose_name='渠道'),
        ),
    ]
