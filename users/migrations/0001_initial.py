# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2019-06-28 18:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=4)),
                ('level', models.IntegerField(default=0)),
                ('access_token', models.CharField(default='', max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=2000)),
                ('phone', models.CharField(blank=True, default='', max_length=200)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to=users.models.get_user_image_path)),
                ('blocked', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PasswordSetter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(default=1)),
                ('browser', models.CharField(blank=True, default='', max_length=500)),
                ('location', models.CharField(blank=True, default='', max_length=500)),
                ('reset_token', models.CharField(blank=True, default='', max_length=200)),
                ('expires_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.CustomUser')),
            ],
        ),
        migrations.AddField(
            model_name='admin',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.CustomUser'),
        ),
    ]
