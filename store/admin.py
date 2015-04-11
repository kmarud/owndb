from django.contrib import admin
from store.models import Project
from store.models import Form
from store.models import Type
from store.models import FormField
from store.models import FormInstance
from store.models import DataText



class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class FormAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class ImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "thumbnail"]


admin.site.register(Project, ProjectAdmin)
admin.site.register(Form, FormAdmin)
admin.site.register(Type)
admin.site.register(FormField)
admin.site.register(FormInstance)
admin.site.register(DataText)
