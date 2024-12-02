from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, LocalizeAccommodation


# Admin configuration for Location model using LeafletGeoAdmin
class LocationAdmin(LeafletGeoAdmin):  # Changed to LeafletGeoAdmin
    list_display = ('id', 'title', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code')
    settings_overrides = {  # Optional: Customize Leaflet map settings
        'DEFAULT_CENTER': (0, 0),  # Latitude and Longitude for default map center
        'DEFAULT_ZOOM': 6,         # Default zoom level
    }


class AccommodationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'country_code', 'usd_rate', 'review_score', 'bedroom_count', 'published', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'location_id__title', 'amenities')
    list_filter = ('published', 'location_id')
    raw_id_fields = ('location_id', 'user_id')
    ordering = ('-created_at',)

    settings_overrides = {  # Optional: Customize Leaflet map settings
        'DEFAULT_CENTER': (0, 0),  # Latitude and Longitude for default map center
        'DEFAULT_ZOOM': 6,         # Default zoom level
    }

    def get_queryset(self, request):
        """Limit queryset to show only accommodations created by the logged-in user for Property Owners."""
        qs = super().get_queryset(request)
        if request.user.groups.filter(name='Property Owners').exists():
            # Show only the accommodations created by the logged-in user
            return qs.filter(user_id=request.user)
        return qs  # Admins can see all accommodations

    def save_model(self, request, obj, form, change):
        """Automatically assign the logged-in user as the creator if not set."""
        if not obj.user_id:
            obj.user_id = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        """Allow Property Owner users to edit only their own accommodations."""
        if obj and obj.user_id != request.user:
            return False  # Restrict Property Owners from editing others' records
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """Allow Property Owner users to delete only their own accommodations."""
        if obj and obj.user_id != request.user:
            return False  # Restrict Property Owners from deleting others' records
        return super().has_delete_permission(request, obj)


class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_id', 'language', 'description')
    search_fields = ('property_id__title', 'language')
    list_filter = ('language',)


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['id', 'email', 'username', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']


# Register models with the admin interface
admin.site.register(Location, LocationAdmin)
admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
