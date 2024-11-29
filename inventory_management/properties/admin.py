from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation


# Register your models here.
class LocationAdmin(admin.ModelAdmin):  # Changed from OSMGeoAdmin to ModelAdmin
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code')


class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country_code', 'usd_rate', 'review_score', 'bedroom_count', 'published', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'location_id__title', 'amenities')
    list_filter = ('published', 'location_id')
    raw_id_fields = ('location_id', 'user_id')
    ordering = ('-created_at',)


class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_id', 'language', 'description')
    search_fields = ('property_id__title', 'language')
    list_filter = ('language',)


# Register models with the admin interface
admin.site.register(Location, LocationAdmin)
admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)
