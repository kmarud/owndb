# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Connection',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConnectionInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('connection', models.ForeignKey(to='store.Connection')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DataText',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('data', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=60)),
                ('slug', models.SlugField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('caption', models.CharField(max_length=200)),
                ('settings', models.CharField(max_length=1000, null=True)),
                ('position', models.IntegerField(default=0)),
                ('form', models.ForeignKey(to='store.Form')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(verbose_name='Data dodania', auto_now_add=True)),
                ('form', models.ForeignKey(to='store.Form')),
                ('user', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=60)),
                ('slug', models.SlugField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sharing',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('form', models.ForeignKey(to='store.Form')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='formfield',
            name='type',
            field=models.ForeignKey(to='store.Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='form',
            name='project',
            field=models.ForeignKey(to='store.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datatext',
            name='formfield',
            field=models.ForeignKey(to='store.FormField'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datatext',
            name='forminstance',
            field=models.ForeignKey(blank=True, null=True, to='store.FormInstance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connectioninstance',
            name='forminstance',
            field=models.ForeignKey(to='store.FormInstance'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connection',
            name='formfield_begin',
            field=models.ForeignKey(to='store.FormField'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='connection',
            name='formfield_end',
            field=models.ForeignKey(to='store.FormField', related_name='ff_end-ff'),
            preserve_default=True,
        ),
    ]
