from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models as gis_models
import json


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


class Accommodation(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    bedroom_count = models.PositiveIntegerField(null=True, blank=True)
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = gis_models.PointField()
    images = models.JSONField()  # JSON array of image URLs
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
    amenities = models.JSONField()  # JSONB array of amenities
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    language = models.CharField(max_length=2)
    description = models.TextField()
    policy = models.JSONField()  # JSONB dictionary for policies

    def __str__(self):
        return f"Localized {self.property_id.title} in {self.language}"
