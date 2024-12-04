from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, LocalizeAccommodation
from .resources import LocationResource


# Admin configuration for Location model using LeafletGeoAdmin
class LocationAdmin(ImportExportModelAdmin, LeafletGeoAdmin):
    resource_class = LocationResource  # Changed to LeafletGeoAdmin
    list_display = ('id', 'title', 'center', 'location_type', 'country_code', 'state_abbr', 'city', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'state_abbr', 'city')
    list_filter = ('location_type', 'country_code')
    # settings_overrides = {  # Optional: Customize Leaflet map settings
    #     'DEFAULT_CENTER': (0, 0),  # Latitude and Longitude for default map center
    #     'DEFAULT_ZOOM': 6,         # Default zoom level
    # }


class AccommodationAdmin(LeafletGeoAdmin):
    list_display = ('id', 'title', 'user_id', 'country_code', 'usd_rate', 'review_score', 'bedroom_count', 'published', 'created_at', 'updated_at')
    search_fields = ('title', 'country_code', 'location_id__title', 'amenities')
    list_filter = ('published', 'location_id')
    raw_id_fields = ('location_id', 'user_id')
    ordering = ('-created_at',)
    autocomplete_fields = ["location_id"]

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

    def get_form(self, request, obj=None, **kwargs):
        """
        Modify the form to set the user_id field as read-only 
        and pre-populate it with the current user for all users.
        """
        form = super().get_form(request, obj, **kwargs)

        # Create a custom form that sets the user_id field as initial and disabled
        class CustomForm(form):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # Set the initial value and disable the field
                self.fields['user_id'].initial = request.user
                self.fields['user_id'].disabled = True
                self.fields['user_id'].widget.attrs['readonly'] = True

        return CustomForm

    def save_model(self, request, obj, form, change):
        """
        Ensure user_id is set for all users during both creation and editing.
        """
        # If user_id is not set, assign the current user
        if not obj.user_id:
            obj.user_id = request.user
        
        super().save_model(request, obj, form, change)


class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property_id', 'language', 'description')
    search_fields = ('property_id__title', 'language')
    list_filter = ('language',)


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['id', 'username', 'email', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff']
    ordering = ('id',)


# Register models with the admin interface
admin.site.register(Location, LocationAdmin)
admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(LocalizeAccommodation, LocalizeAccommodationAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
