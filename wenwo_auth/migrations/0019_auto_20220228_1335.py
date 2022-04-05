# Generated by Django 2.2.3 on 2022-02-28 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wenwo_auth', '0018_user_is_sign'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwalletrecord',
            name='source_type',
            field=models.CharField(choices=[('WeiChat', 'WeiChat'), ('ZhiFuBao', 'ZhiFuBao'), ('InviteReward', 'InviteReward'), ('Register', 'Register'), ('BlogReward', 'BlogReward'), ('QuestionReward', 'QuestionReward'), ('AnswerReward', 'AnswerReward'), ('CourseReward', 'CourseReward'), ('VideoReward', 'VideoReward'), ('FeedBackRewardOutput', 'FeedBackRewardOutput')], default='Register', max_length=16, verbose_name='渠道'),
        ),
    ]
