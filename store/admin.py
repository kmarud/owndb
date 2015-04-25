from django.contrib import admin
from imagekit.admin import AdminThumbnail
from store.models import Image


class ImageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "admin_thumbnail"]
    admin_thumbnail = AdminThumbnail(image_field='thumbnailSmall')

admin.site.register(Image, ImageAdmin)
