# Generated by Django 2.2.7 on 2021-10-21 11:23

import DjangoUeditor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wenwo_auth', '0009_auto_20211021_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('title', models.CharField(max_length=70, verbose_name='反馈标题')),
                ('body', DjangoUeditor.models.UEditorField(blank=True, verbose_name='反馈内容')),
                ('status', models.CharField(choices=[('Accept', 'Accept'), ('Refuse', 'Refuse'), ('UnHandle', 'UnHandle')], default='UnHandle', max_length=100, verbose_name='状态')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否有效')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wenwo_auth.User', verbose_name='反馈的用户')),
            ],
            options={
                'verbose_name': '建议反馈表',
                'verbose_name_plural': '建议反馈表',
            },
        ),
    ]
