# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 12:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20170509_1611'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attractions',
            options={'ordering': ['at_category']},
        ),
        migrations.AddField(
            model_name='attractions',
            name='at_img_url',
            field=models.TextField(null=True),
        ),
    ]
