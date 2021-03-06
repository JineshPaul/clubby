# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-21 07:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20170220_0827'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('address1', models.TextField(blank=True, null=True, verbose_name='address1')),
                ('address2', models.TextField(blank=True, null=True, verbose_name='address2')),
                ('pincode', models.CharField(blank=True, max_length=254, null=True, verbose_name='Pincode ')),
                ('city', models.CharField(blank=True, max_length=254, null=True, verbose_name='City ')),
                ('district', models.CharField(blank=True, max_length=254, null=True, verbose_name='District ')),
                ('state', models.CharField(blank=True, max_length=254, null=True, verbose_name='State ')),
                ('countrty', models.CharField(blank=True, max_length=254, null=True, verbose_name='Country ')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='user',
            name='occupation',
            field=models.CharField(blank=True, choices=[('P', 'Producer'), ('D', 'Director'), ('A', 'Actor'), ('C', 'Choreographer'), ('S', 'Stunt Master')], default='', max_length=1),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
