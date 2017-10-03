# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 16:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


def create_test_user(apps, schema):
    User = apps.get_model(settings.AUTH_USER_MODEL)

    User.objects.create(
        username='testuser',
        email='test@user.uk',
        first_name='Test',
        last_name='User')


def delete_test_user(apps, schema):
    User = apps.get_model(settings.AUTH_USER_MODEL)

    try:
        User.objects.get(username='testuser').delete()
    except User.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demosite', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_test_user, delete_test_user),
    ]
