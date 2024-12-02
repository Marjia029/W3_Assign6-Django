from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.utils.timezone import now
import json


class Location(models.Model):
    # Choices for location types
    LOCATION_TYPES = [
        ('continent', 'Continent'),
        ('country', 'Country'),
        ('state', 'State'),
        ('city', 'City'),
    ]

    id = models.CharField(
        max_length=20,
        primary_key=True,
        help_text="Unique identifier for the location (max 20 characters)."
    )
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        help_text="Name of the location (required, max 100 characters)."
    )
    center = gis_models.PointField(
        help_text="Geolocation of the location (latitude, longitude)."
    )
    parent_id = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sub_locations",
        help_text="Parent location for hierarchical nesting."
    )
    location_type = models.CharField(
        max_length=20,
        choices=LOCATION_TYPES,
        default='city',
        help_text="Type of location (e.g., continent, country, state, city)."
    )
    country_code = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        help_text="ISO country code (optional, max 2 characters).",
        validators=[
            # Optional: You can add a regex validator for ISO 3166-1 alpha-2 codes
        ]
    )
    state_abbr = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        help_text="State abbreviation (optional, max 3 characters)."
    )
    city = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text="City name (optional, max 30 characters)."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the location was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the location was last updated."
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ["title"]


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
    LANGUAGES = [
        ('en', 'English'),
        ('es', 'Spanish'),
        ('fr', 'French'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('ru', 'Russian'),
        ('zh', 'Chinese'),
        # Add more languages as needed
    ]

    id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    language = models.CharField(max_length=2, choices=LANGUAGES)
    description = models.TextField()
    policy = models.JSONField()  # JSONB dictionary for policies

    def __str__(self):
        return f"Localized {self.property_id.title} in {self.language}"

    class Meta:
        verbose_name = "Localized Accommodation"
        verbose_name_plural = "Localized Accommodations"
