from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import hashlib


# Class needed by django-allauth to access account_verified signal in templates
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    class Meta:
        db_table = 'user_profile'

    def account_verified(self):
        if self.user.is_authenticated:
            result = EmailAddress.objects.filter(email=self.user.email)
            if len(result):
                return result[0].verified
        return False

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


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
        if self.type.name == "Text":
            text = self.text_set.all()
            return text
        else:
            return "Błąd"


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