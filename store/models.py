from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from owndb.settings import MEDIA_URL
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import post_delete
from django.utils.html import format_html
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount
import os, hashlib


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


class Project(models.Model):
    title = models.CharField(max_length=60)
    owner = models.ForeignKey(User)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Form(models.Model):
    title = models.CharField(max_length=60)
    project = models.ForeignKey(Project)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Sharing(models.Model):
    form = models.ForeignKey(Form)
    owner = models.ForeignKey(User)
    
    def __str__(self):
        return str(self.pk)
        
        
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
    
    def get_data(self):
        if self.type.name=='Text':
            return self.datatext_set.all()
        elif self.type.name=='Number':
            return self.datatext_set.all()
        elif self.type.name=='Choice':
            return self.datatext_set.all()
        elif self.type.name=='Checkbox':
            return self.datatext_set.all()
        elif self.type.name=='Image':
            return self.image_set.all()
        elif self.type.name=='File':
            return self.image_set.all()
        elif self.type.name=='Connection':
            return ConnectionInstance.objects.filter(connection=Connection.objects.get(formfield=self.pk))
        elif self.type.name=='LabelText':
            return self.datatext_set.all()
        elif self.type.name=='LabelImage':
            return self.image_set.all()
        elif self.type.name=='NextForm':
            return self.datatext_set.all()
        else:
            return None

class FormInstance(models.Model):
    form = models.ForeignKey(Form)
    date = models.DateTimeField('Data dodania', auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    def next_instance(self):
        next_instance = FormInstance.objects.get(pk=self.pk+1)
        if next_instance.form.pk == self.form.pk:
            return next_instance.pk
        else:
            return False

    def prev_instance(self):
        prev_instance = FormInstance.objects.get(pk=self.pk-1)
        if prev_instance.form.pk == self.form.pk:
            return prev_instance.pk
        else:
            return False

            
class Connection(models.Model):
    formfield = models.ForeignKey(FormField)
    form = models.ForeignKey(Form)

    def __str__(self):
        return str(self.pk)
        
 
class ConnectionInstance(models.Model):
    connection = models.ForeignKey(Connection)
    forminstance = models.ForeignKey(FormInstance)
    choseninstance = models.ForeignKey(FormInstance, related_name='chosen_instance')
    
    def display(self):
        form = Connection.objects.get(pk=self.connection.pk).form
        out = "<table><thead><tr>"
        for field in FormField.objects.filter(form=form).order_by('position'):
            if (field.type.pk != 8 and field.type.pk != 9 and field.type.pk != 10 and field.type.pk != 5):
                out += '<td>'+ field.caption +'</td>'
        out += "</tr></thead><tbody>"
        instance = FormInstance.objects.get(pk=self.choseninstance.pk)
        out += '<tr>'
        for field in FormField.objects.filter(form=form).order_by('position'):
            if (field.type.pk != 8 and field.type.pk != 9 and field.type.pk != 10 and field.type.pk != 5):
                insd = DataText.objects.get(formfield = field, forminstance = instance)
                out += '<td>' + str(insd.data) + '</td>'
        out += '</tr></tbody></table>'
        return format_html(out)
        

class DataText(models.Model):
    formfield = models.ForeignKey(FormField)
    forminstance = models.ForeignKey(FormInstance, null=True, blank=True)
    data = models.TextField()

    def display(self):
        type = Type.objects.get(pk=FormField.objects.get(pk=self.formfield.pk).type.pk)
        if type.pk == 1 or type.pk == 2: #text or number
            return format_html('<span>{0}</span>', self.data)
        elif type.pk == 3 or type.pk == 4: #choice or checkbox
            opt = FormField.objects.get(pk=self.formfield.pk).settings.split(';')
            del opt[0]
            ans = self.data.split(';')
            del ans[0]
            temp = ''
            i = 0
            for val in ans:
                if val == '1':
                    temp += str(opt[i]) + '<br />'
                i += 1
            return format_html(temp)
        elif type.pk == 10: #nextform
            return format_html('<span>Here is NextForm button! You shouldn\'t see that!</span>')
        elif type.pk == 8: #labeltext
            return format_html('<h4>{0}</h4>', self.data)
        else:
            return format_html('<span>Unrecognized field type!</span>')
        
        
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
        return format_html('<img class="form_image" border="0" alt="" src="{0}"/>', os.path.join(MEDIA_URL, self.image.name))
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

        
