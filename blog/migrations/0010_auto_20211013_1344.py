# Generated by Django 2.2.7 on 2021-10-13 05:44

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20211011_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=mdeditor.fields.MDTextField(),
        ),
        migrations.AlterField(
            model_name='blogreply',
            name='content',
            field=mdeditor.fields.MDTextField(),
        ),
    ]
