from django.contrib import admin
from store.models import Category
from store.models import Form
from store.models import Type
from store.models import FormField
from store.models import FormInstance
from store.models import Text
from store.models import Boolean
from store.models import Image


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class FormAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class ImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "thumbnail"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Form, FormAdmin)
admin.site.register(Type)
admin.site.register(FormField)
admin.site.register(FormInstance)
admin.site.register(Text)
admin.site.register(Boolean)
admin.site.register(Image, ImageAdmin)