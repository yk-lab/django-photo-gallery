import json
from typing import Any

from django.contrib import admin
from django.forms import ModelForm
from django_admin_search.admin import AdvancedSearchAdmin

from .models import Exif, Photo
from .utils import ExifJSONEncoder


class PhotoSearchForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['file', 'width', 'height']


@admin.register(Photo)
class PhotoAdmin(AdvancedSearchAdmin):
    search_form = PhotoSearchForm
    search_fields = ['id', 'file']
    list_filter = ['file', 'created', 'modified']
    list_display = [
        'id',
        'file',
        'width',
        'height',
        'shooting_datetime',
        'device',
        'place',
        'meta']
    fields = ['id',
              'file',
              'width',
              'height',
              'shooting_datetime',
              'device',
              'place',
              'meta',
              'show_exif']
    readonly_fields = ['id', 'file', 'width', 'height', 'show_exif']

    def show_exif(self, obj):
        return obj.exif.exif

    def save_model(
            self,
            request: Any,
            obj: Photo,
            form: Any,
            change: bool) -> None:
        if not change:
            obj.set_place_from_exif()
            obj.set_shooting_datetime_from_exif()
            obj.set_device_from_exif()

            exif_obj = Exif.objects\
                .create(exif=json.dumps(obj.get_exif, cls=ExifJSONEncoder))
            obj.exif = exif_obj
        super().save_model(request, obj, form, change)
