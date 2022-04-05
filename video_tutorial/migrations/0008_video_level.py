# Generated by Django 2.2.7 on 2021-10-15 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video_tutorial', '0007_auto_20211015_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='level',
            field=models.CharField(choices=[('Rookie', 'Rookie'), ('Primary', 'Primary'), ('Middle', 'Middle'), ('Senior', 'Senior')], default='WeiChat', max_length=16, verbose_name='渠道'),
        ),
    ]