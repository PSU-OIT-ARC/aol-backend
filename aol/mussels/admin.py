from django.contrib import admin


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
