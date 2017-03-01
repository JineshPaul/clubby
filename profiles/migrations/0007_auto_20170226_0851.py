# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-26 08:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20170226_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('S', 'Single'), ('M', 'Married')], max_length=1, null=True),
        ),
    ]