from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from owndb.settings import MEDIA_URL
import os

from django.dispatch import receiver
from django.db.models.signals import post_delete

class Project(models.Model):
    title = models.CharField(max_length=60)
    owner = models.ForeignKey(User)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Projekt"
        verbose_name_plural = "Projekty"

    def __str__(self):
        return self.title


class Form(models.Model):
    title = models.CharField(max_length=60)
    project = models.ForeignKey(Project)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Formularz"
        verbose_name_plural = "Formularze"

    def __str__(self):
        return self.title


class Sharing(models.Model):
    form = models.ForeignKey(Form)
    owner = models.ForeignKey(User)
    
        
class Type(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class FormField(models.Model):
    form = models.ForeignKey(Form)
    type = models.ForeignKey(Type)
    caption = models.CharField(max_length=200)
    settings = models.CharField(max_length=1000, null=True)
    position = models.IntegerField(default=0)
    label = models.BooleanField(default=False, verbose_name='Etykieta')

    def __str__(self):
        return str(self.pk)
            
    def get_data(self):
        data = {
            'Text': self.datatext_set.all(),
        }[self.type.name]
        return data


class FormInstance(models.Model):
    form = models.ForeignKey(Form)
    date = models.DateTimeField('Data dodania', auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

        
class Connection(models.Model):
    formfield = models.ForeignKey(FormField)
    #formfield_connected = models.ForeignKey(FormField)

    def __str__(self):
        return str(self.pk)

        
class DataText(models.Model):
    formfield = models.ForeignKey(FormField)
    forminstance = models.ForeignKey(FormInstance, null=True, blank=True)
    data = models.TextField(verbose_name='Treść')

    def display(self):
        return self.data

        
class ConnectionInstance(models.Model):
    connection = models.ForeignKey(Connection)
    forminstance = models.ForeignKey(FormInstance)
    #content = models.ForeignKey(DataText)
   
    def __str__(self):
        return str(self.pk)   
