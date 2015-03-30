# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Boolean',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('data', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=60)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name_plural': 'Formularze',
                'verbose_name': 'Formularz',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('caption', models.CharField(max_length=200)),
                ('settings', models.CharField(max_length=1000, null=True)),
                ('position', models.IntegerField(default=0)),
                ('label', models.BooleanField(verbose_name='Etykieta', default=False)),
                ('form', models.ForeignKey(to='store.Form')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Data dodania')),
                ('form', models.ForeignKey(to='store.Form')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('image', models.ImageField(upload_to='images')),
                ('formfield', models.ForeignKey(to='store.FormField')),
                ('forminstance', models.ForeignKey(blank=True, to='store.FormInstance', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=60)),
                ('slug', models.SlugField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Projekty',
                'verbose_name': 'Projekt',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('data', models.TextField(verbose_name='Treść')),
                ('formfield', models.ForeignKey(to='store.FormField')),
                ('forminstance', models.ForeignKey(blank=True, to='store.FormInstance', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
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
            model_name='boolean',
            name='formfield',
            field=models.ForeignKey(to='store.FormField'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='boolean',
            name='forminstance',
            field=models.ForeignKey(blank=True, to='store.FormInstance', null=True),
            preserve_default=True,
        ),
    ]
