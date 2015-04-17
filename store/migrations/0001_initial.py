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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('data', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=60)),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Formularz',
                'verbose_name_plural': 'Formularze',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date', models.DateTimeField(verbose_name='Data dodania', auto_now_add=True)),
                ('form', models.ForeignKey(to='store.Form')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('image', models.ImageField(upload_to='images')),
                ('formfield', models.ForeignKey(to='store.FormField')),
                ('forminstance', models.ForeignKey(to='store.FormInstance', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=60)),
                ('slug', models.SlugField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Projekt',
                'verbose_name_plural': 'Projekty',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Text',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('data', models.TextField(verbose_name='Treść')),
                ('formfield', models.ForeignKey(to='store.FormField')),
                ('forminstance', models.ForeignKey(to='store.FormInstance', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=60)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='profile')),
            ],
            options={
                'db_table': 'user_profile',
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
            field=models.ForeignKey(to='store.FormInstance', null=True, blank=True),
            preserve_default=True,
        ),
    ]
