# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-09 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_attractions_at_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attractions',
            name='at_name',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]
