# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-18 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comp', '0008_auto_20161218_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]