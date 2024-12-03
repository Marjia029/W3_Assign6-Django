from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.contrib.messages import get_messages
from django.contrib import messages
from .views import SignupView 
from .models import Location, Accommodation, LocalizeAccommodation


class LocationModelTest(TestCase):
    def setUp(self):
        # Set up test data
        self.parent_location = Location.objects.create(
            id="continent-01",
            title="Asia",
            center=Point(100.0, 20.0),
            location_type="continent"
        )
        self.child_location = Location.objects.create(
            id="country-01",
            title="India",
            center=Point(77.0, 28.0),
            parent_id=self.parent_location,
            location_type="country",
            country_code="IN"
        )

    def test_location_creation(self):
        """Test that a Location instance is created correctly."""
        location = Location.objects.get(id="continent-01")
        self.assertEqual(location.title, "Asia")
        self.assertEqual(location.location_type, "continent")
        self.assertIsNone(location.parent_id)
        self.assertEqual(location.center.x, 100.0)
        self.assertEqual(location.center.y, 20.0)

    def test_hierarchical_relationship(self):
        """Test that parent-child relationships work correctly."""
        child = Location.objects.get(id="country-01")
        self.assertEqual(child.parent_id, self.parent_location)
        self.assertEqual(child.parent_id.title, "Asia")

    def test_field_defaults(self):
        """Test default values for fields."""
        location = Location.objects.create(
            id="city-01",
            title="Tokyo",
            center=Point(139.6917, 35.6895)
        )
        self.assertEqual(location.location_type, "city")
        self.assertIsNone(location.country_code)
        self.assertIsNone(location.state_abbr)
        self.assertIsNone(location.parent_id)

    def test_geo_point_field(self):
        """Test that the PointField stores correct geographic data."""
        location = Location.objects.get(id="continent-01")
        self.assertEqual(location.center.x, 100.0)
        self.assertEqual(location.center.y, 20.0)

    def test_string_representation(self):
        """Test the string representation of the model."""
        location = Location.objects.get(id="continent-01")
        self.assertEqual(str(location), "Asia")

    def test_ordering(self):
        """Test that locations are ordered by title."""
        Location.objects.create(
            id="city-02",
            title="Beijing",
            center=Point(116.4074, 39.9042),
            location_type="city"
        )
        locations = Location.objects.all()
        titles = [location.title for location in locations]
        self.assertEqual(titles, ["Asia", "Beijing", "India"])


User = get_user_model()


class AccommodationModelTest(TestCase):
    def setUp(self):
        # Create required related objects
        self.location = Location.objects.create(
            id="location-01",
            title="Paris",
            center=Point(2.3522, 48.8566),
            location_type="city",
            country_code="FR"
        )

        # Create a custom user
        self.user = User.objects.create_user(
            username="testuser", 
            password="password123",
            email="testuser@example.com"
        )

        # Create an accommodation object
        self.accommodation = Accommodation.objects.create(
            id="accommodation-01",
            title="Cozy Apartment in Paris",
            country_code="FR",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=150.00,
            center=Point(2.3522, 48.8566),
            images=["image1.jpg", "image2.jpg"],
            location_id=self.location,
            amenities=["WiFi", "Air Conditioning"],
            user_id=self.user,
            published=True
        )

    def test_accommodation_creation(self):
        """Test that an Accommodation instance is created correctly."""
        accommodation = Accommodation.objects.get(id="accommodation-01")
        self.assertEqual(accommodation.title, "Cozy Apartment in Paris")
        self.assertEqual(accommodation.country_code, "FR")
        self.assertEqual(accommodation.bedroom_count, 2)
        self.assertEqual(accommodation.review_score, 4.5)
        self.assertEqual(accommodation.usd_rate, 150.00)
        self.assertTrue(accommodation.published)
        self.assertEqual(accommodation.images, ["image1.jpg", "image2.jpg"])
        self.assertEqual(accommodation.amenities, ["WiFi", "Air Conditioning"])

    def test_relationship_with_location(self):
        """Test the relationship between Accommodation and Location."""
        accommodation = Accommodation.objects.get(id="accommodation-01")
        self.assertEqual(accommodation.location_id, self.location)
        self.assertEqual(accommodation.location_id.title, "Paris")

    def test_relationship_with_user(self):
        """Test the relationship between Accommodation and the custom User."""
        accommodation = Accommodation.objects.get(id="accommodation-01")
        self.assertEqual(accommodation.user_id, self.user)
        self.assertEqual(accommodation.user_id.username, "testuser")
        self.assertEqual(accommodation.user_id.email, "testuser@example.com")

    def test_field_defaults(self):
        """Test default values for certain fields."""
        accommodation = Accommodation.objects.create(
            id="accommodation-02",
            title="Minimalist Studio",
            country_code="FR",
            usd_rate=80.00,
            center=Point(2.3522, 48.8566),
            location_id=self.location,
            amenities=[],
            images=[]
        )
        self.assertEqual(accommodation.feed, 0)
        self.assertEqual(accommodation.review_score, 0.0)
        self.assertFalse(accommodation.published)
        self.assertIsNone(accommodation.user_id)

    def test_geo_point_field(self):
        """Test that the PointField stores geographic data correctly."""
        accommodation = Accommodation.objects.get(id="accommodation-01")
        self.assertEqual(accommodation.center.x, 2.3522)
        self.assertEqual(accommodation.center.y, 48.8566)

    def test_string_representation(self):
        """Test the string representation of the model."""
        accommodation = Accommodation.objects.get(id="accommodation-01")
        self.assertEqual(str(accommodation), "Cozy Apartment in Paris")

    def test_json_field_handling(self):
        """Test the JSONField for images and amenities."""
        accommodation = Accommodation.objects.get(id="accommodation-01")
        self.assertIn("image1.jpg", accommodation.images)
        self.assertIn("WiFi", accommodation.amenities)

    def test_ordering(self):
        """Test that accommodations can be ordered correctly by a custom field."""
        Accommodation.objects.create(
            id="accommodation-03",
            title="Luxury Penthouse",
            country_code="FR",
            usd_rate=500.00,
            center=Point(2.3522, 48.8566),
            location_id=self.location,
            amenities=["Beachfront", "Private Pool"],
            images=[]
        )
        accommodations = Accommodation.objects.order_by("-usd_rate")
        self.assertEqual(accommodations.first().title, "Luxury Penthouse")


class LocalizeAccommodationModelTest(TestCase):
    def setUp(self):
        # Set up a location instance
        self.location = Location.objects.create(
            id="location-01",
            title="Paris",
            center=Point(2.3522, 48.8566),
            location_type="city",
            country_code="FR"
        )

        # Set up an accommodation instance
        self.accommodation = Accommodation.objects.create(
            id="accommodation-01",
            feed=1,
            title="Luxury Penthouse",
            country_code="FR",
            usd_rate=500.00,
            center=Point(2.3522, 48.8566),
            images=["image1.jpg", "image2.jpg"],
            location_id=self.location,
            amenities=["WiFi", "Pool"],
            published=True
        )

    def test_create_localized_accommodation(self):
        # Create a localized accommodation with valid data
        policy_data = {"check_in": "3 PM", "check_out": "11 AM"}
        localized_accommodation = LocalizeAccommodation.objects.create(
            property_id=self.accommodation,
            language="fr",
            description="Un penthouse luxueux au cœur de Paris.",
            policy=policy_data
        )

        # Verify the instance is saved and fields are correct
        self.assertEqual(localized_accommodation.language, "fr")
        self.assertEqual(localized_accommodation.description, "Un penthouse luxueux au cœur de Paris.")
        self.assertEqual(localized_accommodation.policy, policy_data)

    def test_policy_field_required(self):
        # Attempt to create a localized accommodation without a policy
        with self.assertRaises(ValidationError):
            localized_accommodation = LocalizeAccommodation(
                property_id=self.accommodation,
                language="fr",
                description="Un penthouse luxueux au cœur de Paris."
            )
            localized_accommodation.full_clean()  # Trigger validation checks

    def test_language_field_choices(self):
        # Attempt to create a localized accommodation with an invalid language code
        with self.assertRaises(ValidationError):
            localized_accommodation = LocalizeAccommodation(
                property_id=self.accommodation,
                language="xx",  # Invalid language code
                description="An invalid language test case.",
                policy={"check_in": "3 PM", "check_out": "11 AM"}
            )
            localized_accommodation.full_clean()  # Trigger validation checks

    def test_str_method(self):
        # Create a localized accommodation and verify the string representation
        localized_accommodation = LocalizeAccommodation.objects.create(
            property_id=self.accommodation,
            language="fr",
            description="Un penthouse luxueux au cœur de Paris.",
            policy={"check_in": "3 PM", "check_out": "11 AM"}
        )
        self.assertEqual(
            str(localized_accommodation),
            "Localized Luxury Penthouse in fr"
        )


class IndexViewTest(TestCase):

    def test_index_view(self):
        # Test that the Index view renders correctly
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class SignupViewTestCase(TestCase):
    def setUp(self):
        """
        Set up test data and configurations before each test
        """
        self.client = Client()
        self.signup_url = reverse('signup')  # Ensure this matches your URL name
        
        # Create the Property Owners group before tests
        self.property_owners_group, created = Group.objects.get_or_create(name='Property Owners')
    
    def test_signup_view_get(self):
        """
        Test that the signup page loads correctly
        """
        response = self.client.get(self.signup_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed(response, 'signup.html')
    
    def test_valid_signup_form(self):
        """
        Test successful user signup
        """
        signup_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!'
        }
        
        response = self.client.post(self.signup_url, data=signup_data)
        
        # Check redirect
        self.assertRedirects(response, reverse('login'))
        
        # Verify user creation
        user = User.objects.get(username='testuser')
        self.assertIsNotNone(user)
        self.assertFalse(user.is_active)  # Ensure user is inactive
        
        # Check group assignment
        self.assertIn(self.property_owners_group, user.groups.all())
        
        # Check messages
        messages_list = list(messages.get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(
            messages_list[0].message, 
            'Your account has been created successfully. Wait for admin activation.'
        )
    
    def test_invalid_signup_form(self):
        """
        Test signup with invalid form data
        """
        invalid_data_sets = [
            # Mismatched passwords
            {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password1': 'ComplexPassword123!',
                'password2': 'DifferentPassword456!'
            },
            # Weak password
            {
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password1': 'weak',
                'password2': 'weak'
            },
            # Empty fields
            {
                'username': '',
                'email': '',
                'password1': '',
                'password2': ''
            }
        ]
        
        for invalid_data in invalid_data_sets:
            response = self.client.post(self.signup_url, data=invalid_data)
            
            # Ensure form is not valid and user is not created
            self.assertEqual(response.status_code, 200)  # Should return to signup page
            self.assertFalse(User.objects.filter(username=invalid_data.get('username')).exists())
            self.assertIn('form', response.context)
            self.assertTrue(response.context['form'].errors)  # Form should have validation errors
    
    def test_duplicate_username(self):
        """
        Test signup with existing username
        """
        # Create an existing user
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='ExistingPassword123!'
        )
        
        duplicate_data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!'
        }
        
        response = self.client.post(self.signup_url, data=duplicate_data)
        
        # Ensure user is not created
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)  # Should have username already exists error
    
    def test_missing_property_owners_group(self):
        """
        Test scenario where Property Owners group does not exist
        """
        # Delete the Property Owners group
        Group.objects.filter(name='Property Owners').delete()
        
        signup_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'ComplexPassword123!',
            'password2': 'ComplexPassword123!'
        }
        
        response = self.client.post(self.signup_url, data=signup_data)
        
        # Check that the response is a 200 OK (form re-rendered)
        self.assertEqual(response.status_code, 200)
        
        # Verify no user was created
        self.assertFalse(User.objects.filter(username='testuser').exists())
        
        # Check messages
        messages_list = list(messages.get_messages(response.wsgi_request))
        
        # Debug print
        print("All Messages:", [f"{msg.level}: {msg.message}" for msg in messages_list])
        
        # Filter for error messages
        error_messages = [msg for msg in messages_list if msg.level == messages.ERROR]
        
        # Verify error messages content
        self.assertTrue(error_messages, "No error messages found")
        
        # Check if any error message contains the group missing text
        group_error_exists = any(
            'Property Owners group does not exist' in msg.message 
            for msg in error_messages
        )
        self.assertTrue(group_error_exists, "No message about missing Property Owners group found")
        
        # Ensure no success messages
        success_messages = [msg for msg in messages_list if msg.level == messages.SUCCESS]
        self.assertEqual(len(success_messages), 0)
    
    def test_signup_view_permissions(self):
        """
        Verify that the signup view is publicly accessible
        """
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
