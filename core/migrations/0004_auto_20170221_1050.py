# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-21 10:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_movie_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=254, verbose_name='Cast Name ')),
                ('real_name', models.CharField(max_length=254, verbose_name='Real name ')),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='category',
            field=models.CharField(blank=True, choices=[('D', 'Drama'), ('A', 'Action'), ('T', 'Thriller'), ('F', 'Fantacy'), ('C', 'Animation')], default='', max_length=1),
        ),
        migrations.AddField(
            model_name='cast',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Movie'),
        ),
    ]
