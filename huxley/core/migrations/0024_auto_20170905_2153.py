# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-05 21:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20170809_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.TextField(blank=True, default=b'', null=True)),
                ('published_summary', models.TextField(blank=True, default=b'', null=True)),
                ('voting', models.BooleanField(default=False)),
                ('session_one', models.BooleanField(default=False)),
                ('session_two', models.BooleanField(default=False)),
                ('session_three', models.BooleanField(default=False)),
                ('session_four', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'assignmentsummary',
            },
        ),
        migrations.RemoveField(
            model_name='delegate',
            name='published_summary',
        ),
        migrations.RemoveField(
            model_name='delegate',
            name='session_four',
        ),
        migrations.RemoveField(
            model_name='delegate',
            name='session_one',
        ),
        migrations.RemoveField(
            model_name='delegate',
            name='session_three',
        ),
        migrations.RemoveField(
            model_name='delegate',
            name='session_two',
        ),
        migrations.RemoveField(
            model_name='delegate',
            name='summary',
        ),
        migrations.RemoveField(
            model_name='delegate',
            name='voting',
        ),
        migrations.AddField(
            model_name='assignment',
            name='school',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.School'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='assignment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Assignment'),
        ),
    ]