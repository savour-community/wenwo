# Generated by Django 2.2.3 on 2022-02-07 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_auto_20211213_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_sync',
            field=models.BooleanField(default=False, verbose_name='是否已同步'),
        ),
    ]
