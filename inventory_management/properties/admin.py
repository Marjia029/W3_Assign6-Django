from django.contrib import admin
from .models import Location


# Register your models here.
class LocationAdmin(admin.ModelAdmin):  # Changed from OSMGeoAdmin to ModelAdmin
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code')


admin.site.register(Location, LocationAdmin)
