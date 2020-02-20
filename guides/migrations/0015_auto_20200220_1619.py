# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-02-20 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0014_add_remote_questions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='remote',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', max_length=32, verbose_name='Will you be attending remotely?'),
        ),
    ]