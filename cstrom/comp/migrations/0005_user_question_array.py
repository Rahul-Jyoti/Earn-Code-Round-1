# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 04:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comp', '0004_auto_20161217_0932'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='question_array',
            field=models.TextField(null=True),
        ),
    ]