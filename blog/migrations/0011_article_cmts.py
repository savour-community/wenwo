# Generated by Django 2.2.7 on 2021-10-14 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20211013_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cmts',
            field=models.PositiveIntegerField(default=0, verbose_name='评论次数'),
        ),
    ]