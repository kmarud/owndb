from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=60)
    owner = models.ForeignKey(User)

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return self.title


class Form(models.Model):
    title = models.CharField(max_length=60)
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name = "Formularz"
        verbose_name_plural = "Formularze"

    def __str__(self):
        return self.title


class FormField(models.Model):
    form = models.ForeignKey(Form)
    type = models.ForeignKey(Type)
    field = models.IntegerField()

    def __str__(self):
        return self.text


class Type(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Text(models.Model):
    data = models.TextField(verbose_name='Treść')
    editable = models.BooleanField()

    def __str__(self):
        return self.data


class Boolean(models.Model):
    data = models.BooleanField()