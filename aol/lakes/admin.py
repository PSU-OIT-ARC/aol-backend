from django.contrib.admin.filters import SimpleListFilter
from django.contrib import admin
from django.db.models import Q
from django import forms

from ckeditor.widgets import CKEditorWidget

from aol.photos.admin import PhotoInline
from aol.documents.admin import DocumentInline
from aol.resources.admin import ResourceInline


class LakeForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is not None:
            self.fields['photo'].queryset = self.fields['photo'].queryset.filter(lake=self.instance)


class LakeAdmin(admin.ModelAdmin):
    actions = ['populate_cover_photo']

    list_display = ('reachcode', 'get_name', 'parent',
                    'permanent_id', 'gnis_id',
                    'waterbody_type',
                    'aol_page',
                    'has_mussels', 'has_plants',
                    'has_photos', 'has_docs', 'has_resources')
    list_display_links = ('reachcode', )
    list_filter = ('is_major', 'waterbody_type',
                   'has_docs', 'has_photos', 'has_plants', 'has_mussels')

    search_fields = ('reachcode', 'permanent_id', 'gnis_id', 'gnis_name', 'aol_page')
    raw_id_fields = ('parent',)
    readonly_fields = ('has_plants', 'has_mussels',
                       'has_photos', 'has_docs', 'has_resources')

    filter_horizontal = ('county_set',)

    form = LakeForm
    fieldsets = (
        (None, {
            'fields': ('title', 'body', 'aol_page', 'photo')
        }),
        ('Associations', {
            'fields': ('fishing_zone', 'county_set')
        }),
        ('Indexing information', {
            'fields': ('reachcode', 'permanent_id', 'parent',
                       'gnis_id', 'gnis_name')
        }),
        ('Properties', {
            'fields': ('has_plants', 'has_mussels',
                       'has_photos', 'has_docs', 'has_resources')
        })
    )
    inlines = [
        PhotoInline,
        DocumentInline,
        ResourceInline
    ]

    def has_mussels(self, obj):
        return obj.has_mussels

    def has_plants(self, obj):
        return obj.has_plants

    def has_photos(self, obj):
        return obj.has_photos

    def has_documents(self, obj):
        return obj.has_documents

    def has_resources(self, obj):
        return obj.has_resources

    def get_name(self, obj):
        if obj.title:
            return obj.title
        elif obj.gnis_name:
            return obj.gnis_name
        return '-'
    get_name.short_description = 'Name'

    def populate_cover_photo(self, request, queryset):
        """
        Performs cover photo population via a naive selection.
        """
        for lake in queryset.iterator():
            photo_queryset = lake.photos.order_by('-taken_on')
            lake.photo = photo_queryset.first()
            lake.save()
