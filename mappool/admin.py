from django.contrib import admin
from .models import Map
from .extra_logic.maps import MapPool


# A ghetto way to manually fetch from the sheet, just in case
def update_db(modeladmin, request, queryset):
    def fetchMaps():
        Pool = MapPool()
        Pool.fetchMapsIntoJson()


class MapAdmin(admin.ModelAdmin):
    actions = [update_db]


admin.site.register(Map, MapAdmin)
