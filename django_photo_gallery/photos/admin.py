from django.contrib import admin
from django.forms import ModelForm
from django_admin_search.admin import AdvancedSearchAdmin

from .models import Photo


class PhotoSearchForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['file']


@admin.register(Photo)
class PhotoAdmin(AdvancedSearchAdmin):
    search_form = PhotoSearchForm
    search_fields = ['id', 'file']
    list_filter = ['file', 'created', 'modified']
