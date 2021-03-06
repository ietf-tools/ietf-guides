# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-28 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0010_populate_short'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='groups',
            field=models.CharField(help_text='see <a href="https://www.ietf.org/how/wgs">https://www.ietf.org/how/wgs</a>', max_length=256, verbose_name='Which working groups are you most interested in?'),
        ),
    ]
