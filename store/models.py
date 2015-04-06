from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
import os

# Image type
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from owndb.settings import MEDIA_URL
from django.dispatch import receiver
from django.db.models.signals import post_delete


class Category(models.Model):
    title = models.CharField(max_length=60)
    owner = models.ForeignKey(User)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.title


class Form(models.Model):
    title = models.CharField(max_length=60)
    category = models.ForeignKey(Category)
    slug = models.SlugField()

    class Meta:
        verbose_name = "Formularz"
        verbose_name_plural = "Formularze"

    def __str__(self):
        return self.title


class Type(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class FormInstance(models.Model):
    form = models.ForeignKey(Form)
    date = models.DateTimeField('Data dodania', auto_now_add=True)

    def __str__(self):
        return str(self.pk)


class FormField(models.Model):
    form = models.ForeignKey(Form)
    type = models.ForeignKey(Type)
    position = models.IntegerField(default=0)
    label = models.BooleanField(default=False, verbose_name='Etykieta')

    def __str__(self):
        return str(self.pk)

    def get_data(self):
        data = {
            'Text': self.text_set.all(),
            'Image': self.image_set.all(),
        }[self.type.name]
        return data


class Text(models.Model):
    formfield = models.ForeignKey(FormField)
    forminstance = models.ForeignKey(FormInstance, null=True, blank=True)
    data = models.TextField(verbose_name='Treść')

    def display(self):
        return self.data


class Boolean(models.Model):
    formfield = models.ForeignKey(FormField)
    forminstance = models.ForeignKey(FormInstance, null=True, blank=True)
    data = models.BooleanField(default=False)


class Image(models.Model):
    formfield = models.ForeignKey(FormField)
    forminstance = models.ForeignKey(FormInstance, null=True, blank=True)
    image = models.ImageField(upload_to='images')
    thumbnailSmall = ImageSpecField(source='image',
                                    processors=[ResizeToFill(50, 50)],
                                    format='JPEG',
                                    options={'quality': 80})

    def __str__(self):
        return self.image.name

    def display(self):
        return format_html('<img border="0" alt="" src="{0}"/>', os.path.join(MEDIA_URL, self.image.name))
    display.allow_tags = True


# Automatically delete photo file when database object is being deleted
@receiver(post_delete, sender=Image)
def photo_post_delete_handler(sender, **kwargs):
    photo = kwargs['instance']
    storage, path = photo.image.storage, photo.image.path
    storage.delete(path)
    storage, path = photo.thumbnailSmall.storage, photo.thumbnailSmall.path
    storage.delete(path)
    # Delete empty folder created by django-imagekit
    os.rmdir(os.path.dirname(path))