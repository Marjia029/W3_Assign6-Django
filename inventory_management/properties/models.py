from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models as gis_models


class Location(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    center = gis_models.PointField()
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    location_type = models.CharField(max_length=20)
    country_code = models.CharField(max_length=2, blank=True, null=True)  # Make this optional
    state_abbr = models.CharField(max_length=3, blank=True, null=True)  # Make this optional
    city = models.CharField(max_length=30, blank=True, null=True)  # Make this optional
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

