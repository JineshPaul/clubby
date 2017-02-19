# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-19 12:03
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import profiles.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='user id')),
                ('first_name', models.CharField(blank=True, default='', max_length=254, verbose_name='first name')),
                ('middle_name', models.CharField(blank=True, default='', max_length=254, verbose_name='middle name')),
                ('last_name', models.CharField(blank=True, default='', max_length=254, verbose_name='last name')),
                ('username', models.CharField(max_length=254, unique=True, verbose_name='username')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '9999999999'. Up to 12 digits allowed.", regex='[0-9]{10,12}')], verbose_name='phone_number')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='dob')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect it instead of deleting accounts.', verbose_name='active')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', profiles.manager.CustomUserManager()),
            ],
        ),
    ]
