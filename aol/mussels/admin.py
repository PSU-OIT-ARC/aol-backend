from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib import admin
from django.conf.urls import url
from django.urls import reverse
from django import http, forms

from aol.mussels.tasks import import_mussel_observation_datafile


class MusselAdmin(admin.ModelAdmin):
    list_display = ('name', 'machine_name', 'is_scientific_name')
    list_filter = ('is_scientific_name',)


class MusselObservationAdmin(admin.ModelAdmin):
    list_display = ('lake', 'mussel', 'date_sampled',
                    'target', 'collecting_agency', 'collection_method')
    list_filter = ('mussel', 'collecting_agency', 'target', 'collection_method')
    date_hierarchy = 'date_sampled'

    search_fields = ('lake__title', 'lake__reachcode')
    raw_id_fields = ('lake', 'mussel')


class ImportedMusselObservationAdmin(admin.ModelAdmin):
    actions = ['load_csv']

    list_display = ('name', 'datafile', 'status', 'created_on', 'updated_on')
    readonly_fields = ('status', 'output')
    date_hierarchy = 'created_on'

    fieldsets = (
        (None, {
            'fields': ('datafile', 'status')
        }),
        ('Logging information', {
            'classes': ('collapse',),
            'fields': ('output',)
        }),
    )

    def load_csv(self, request, queryset):
        for obj in queryset.iterator():
            import_mussel_observation_datafile.delay(pk=obj.pk)
            messages.success(request, "CSV import '{}' has been started.".format(obj))
        return http.HttpResponseRedirect(reverse('admin:mussels_importedmusselobservation_changelist'))

    def name(self, obj):
        return str(obj)
    name.short_description = 'Name'
