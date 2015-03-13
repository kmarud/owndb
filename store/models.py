from django.db import models
from django.contrib.auth.models import User


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


class Text(models.Model):
    formfield = models.ForeignKey(FormField)
    forminstance = models.ForeignKey(FormInstance, null=True, blank=True)
    data = models.TextField(verbose_name='Treść')

    def __str__(self):
        return self.data


class Boolean(models.Model):
    formfield = models.ForeignKey(FormField)
    forminstance = models.ForeignKey(FormInstance, null=True, blank=True)
    data = models.BooleanField(default=False)