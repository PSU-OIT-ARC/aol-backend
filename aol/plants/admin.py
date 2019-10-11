from django.views.generic.edit import FormView
from django.core.management import call_command
from django.contrib import messages
from django.contrib import admin
from django.conf.urls import url
from django.urls import reverse
from django import http, forms

from aol.plants.tasks import import_plant_observation_datafile


class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'common_name', 'is_native', 'noxious_weed_designation')
    list_filter = ('is_native', 'noxious_weed_designation')
    search_fields = ('name', 'common_name')


class PlantObservationAdmin(admin.ModelAdmin):
    list_display = ('plant', 'lake_display', 'observation_date', 'source', 'survey_org')
    list_filter = ('source',)
    date_hierarchy = 'observation_date'

    search_fields = ('lake__title', 'lake__reachcode')
    raw_id_fields = ('lake', 'plant')

    def lake_display(self, obj):
        return str(obj.lake) or obj.lake.reachcode
    lake_display.short_description = 'Lake'


class ImportedPlantObservationAdmin(admin.ModelAdmin):
    actions = ['load_csv']

    list_display = ('name', 'datafile', 'source', 'status', 'created_on', 'updated_on')
    readonly_fields = ('status', 'output')
    date_hierarchy = 'created_on'

    fieldsets = (
        (None, {
            'fields': ('source', 'datafile', 'status')
        }),
        ('Logging information', {
            'classes': ('collapse',),
            'fields': ('output',)
        }),
    )


    def load_csv(self, request, queryset):
        for obj in queryset.iterator():
            import_plant_observation_datafile.delay(pk=obj.pk)
            messages.success(request, "CSV import '{}' has been started.".format(obj))
        return http.HttpResponseRedirect(reverse('admin:plants_importedplantobservation_changelist'))

    def name(self, obj):
        return str(obj)
    name.short_description = 'Name'
