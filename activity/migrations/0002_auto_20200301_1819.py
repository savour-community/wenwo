# Generated by Django 2.2.3 on 2020-03-01 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='account_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='activity',
            name='account_name',
            field=models.CharField(default='wenwo', max_length=70),
        ),
    ]
