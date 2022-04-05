# Generated by Django 2.2.3 on 2020-02-16 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='like',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='BlogReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('blog_id', models.IntegerField(default=0)),
                ('reply_id', models.IntegerField(default=0)),
                ('account_id', models.IntegerField(default=0)),
                ('like', models.PositiveIntegerField(default=0)),
                ('content', models.TextField(blank=True, max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]