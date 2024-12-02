# properties/management/commands/generate_sitemap.py
from django.core.management.base import BaseCommand
from properties.models import Location
from django.template.defaultfilters import slugify  # Import slugify
import json
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Generates a sitemap.json file for all country, state, and city locations'

    def handle(self, *args, **kwargs):
        # Get all country locations (location_type = 'country')
        countries = Location.objects.filter(location_type='country').prefetch_related('sub_locations')

        sitemap = []

        # Loop through each country
        for country in countries:
            country_slug = slugify(country.title)  # Slugify country title
            country_data = {
                country.title: country_slug,  # Use the slugged country title
                'locations': []
            }

            # Fetch states (location_type = 'state') under the country
            states = country.sub_locations.filter(location_type='state').order_by('title')
            for state in states:
                state_slug = slugify(state.title)
                state_url = f"{country_slug}/{state_slug}"

                # Add state to locations
                state_data = {state_slug: state_url}
                country_data['locations'].append(state_data)

                # Fetch cities (location_type = 'city') under the state
                cities = state.sub_locations.filter(location_type='city').order_by('title')
                for city in cities:
                    city_slug = slugify(city.title)

                    # If the parent of the city is a state, the URL will be country_slug/state_slug/city_slug
                    city_url = f"{country_slug}/{state_slug}/{city_slug}"

                    city_data = {city_slug: city_url}
                    state_data.setdefault('locations', []).append(city_data)  # Add city under state

            # Fetch cities directly under the country (no state parent)
            cities = country.sub_locations.filter(location_type='city').order_by('title')
            for city in cities:
                city_slug = slugify(city.title)

                # If the parent of the city is a country, the URL will be country_slug/city_slug
                city_url = f"{country_slug}/{city_slug}"

                city_data = {city_slug: city_url}
                country_data['locations'].append(city_data)

            # Sort locations (states and cities) alphabetically by title
            country_data['locations'] = sorted(country_data['locations'], key=lambda x: list(x.keys())[0])

            sitemap.append(country_data)

        # Sort countries alphabetically by title
        sitemap = sorted(sitemap, key=lambda x: list(x.keys())[0])

        # Create the output file path
        output_file = os.path.join(settings.BASE_DIR, 'sitemap.json')

        # Write to the sitemap.json file
        with open(output_file, 'w') as f:
            json.dump(sitemap, f, indent=4)

        self.stdout.write(self.style.SUCCESS('Successfully generated sitemap.json'))
