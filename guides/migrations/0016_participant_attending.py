# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-11-08 04:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0015_auto_20200220_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='attending',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='NO', max_length=32, verbose_name='Will you be attending the next IETF?'),
        ),
    ]
