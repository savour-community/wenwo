# Generated by Django 2.2.7 on 2021-10-10 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wenwo_auth', '0004_auto_20200301_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_times',
            field=models.IntegerField(default=0),
        ),
    ]
