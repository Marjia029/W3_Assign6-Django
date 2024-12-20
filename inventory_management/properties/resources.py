from import_export import resources
from .models import Location


class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
        fields = (
            'id',
            'title',
            'center',
            'parent_id',
            'location_type',
            'country_code', 
            'state_abbr', 
            'city', 
            'created_at', 
            'updated_at'
        )
        export_order = fields  # Optional: Maintain order of fields in export
