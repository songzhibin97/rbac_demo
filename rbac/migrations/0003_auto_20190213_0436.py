# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-02-13 04:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0002_auto_20190213_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='userinfo',
            unique_together=set([]),
        ),
    ]
