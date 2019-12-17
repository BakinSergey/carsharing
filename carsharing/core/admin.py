from core.models import InteriorGallery, Car, ExteriorGallery, csUser
from django.contrib import admin
from django.utils.html import format_html

# Register your models here.


class ExteriorGalleryInline(admin.TabularInline):
    fk_name = 'car'
    model = ExteriorGallery

    def image_tag(self, obj):
        return format_html('<img src="{}" width="120" height="80" />'.format(obj.image.url))

    image_tag.short_description = 'Exterior Image'
    readonly_fields = ('image_tag',)


class InteriorGalleryInline(admin.TabularInline, ):
    fk_name = 'car'
    model = InteriorGallery

    def image_tag(self, obj):
        return format_html('<img src="{}" width="120" height="80" />'.format(obj.image.url))

    image_tag.short_description = 'Interior Image'
    readonly_fields = ('image_tag',)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [ExteriorGalleryInline, InteriorGalleryInline, ]
    readonly_fields = ['params', ]


admin.site.register(csUser)

