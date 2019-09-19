from django.contrib import admin


class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'common_name', 'is_native', 'noxious_weed_designation')
    list_filter = ('is_native', 'noxious_weed_designation')
    search_fields = ('name', 'common_name')


class PlantObservationAdmin(admin.ModelAdmin):
    list_display = ('lake', 'plant', 'observation_date', 'source', 'survey_org')
    list_filter = ('source',)
    date_hierarchy = 'observation_date'

    search_fields = ('lake__title', 'lake__reachcode')
    raw_id_fields = ('lake', 'plant')
