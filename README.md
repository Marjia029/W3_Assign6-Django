# Django Property Management System

---

## Project Overview

This project is a **Property Management System** built using Django, PostgreSQL, and the PostGIS extension. It allows users to manage property information via the Django Admin interface, while incorporating geospatial data capabilities for managing property locations.

---

## Features

1. **Database Support**:
   - PostgreSQL configured with PostGIS for geospatial data management.

2. **Models**:
   - **Location**: Handles hierarchical geolocation data (e.g., countries, cities).
   - **Accommodation**: Manages property details, including geolocation, pricing, amenities, and more.
   - **LocalizeAccommodation**: Provides multi-language support for property descriptions and policies.

3. **Admin Panel Integration**:
   - Property and location data management.
   - Filtering and searching options for quick access.

4. **User Groups**:
   - A **Property Owners** user group, allowing restricted access to manage their own properties.

5. **Frontend**:
   - Public-facing page for property owners to submit sign-up requests.

6. **Command-Line Utility**:
   - Generates a `sitemap.json` file for all country locations.

---

## Prerequisites

- Python 3+
- Django 4.0+
- Docker 

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Marjia029/W3_Assign6-Django.git
   cd 3_Assign6-Django
   ```
2. **Create and Activate Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows
    ```
3. **Configure the PostgreSQL Database with PostGIS**:

   Make sure you have Docker installed in your PC. If you don't have Docker installed, please install Docker first. You can check the [Docker Docs](https://docs.docker.com)  to install Docker in your PC.

   If you are using Windows OS, make sure you have Docker Desktop open before running these commands.
   ```bash
   cd inventory_management
   docker-compose up --build
   ```

      Now open another terminal and run the command
   ```bash
   docker ps
   ```
      Now you can see the list of docker containers that are running. Now Restart your PC and run again
   ```bash
   docker-compose up --build
   ```
   now click http://localhost:8000  to see your application running. You will see an interface like
   
   ![Django Application](./images/Screenshot%20from%202024-12-04%2016-38-18.png)

4. **Run Migrations**:

   In terminal run the commands
   ```bash
   docker exec -it inventory_management-web-1 python manage.py makemigrations 
   docker exec -it inventory_management-web-1 python manage.py migrate
   ```
---

## Usage
 -  Access the Django Admin at http://127.0.0.1:8000/admin.
 - Sign up as a Property Owner from the frontend.
 - Submit property data and manage it via the admin panel.


1. **Create Super User**:

   
   ```bash
   docker exec -it inventory_management-web-1 python manage.py createsuperuser 
   ```

   Enter valiid information about superuser and create superuser

   ![Superuser](./images/Screenshot%20from%202024-12-04%2016-55-55.png)

2. **Login to Django Admin Panel**:
  
   Navigate to the [Django Admin Panel](https://localhost:8000/admin) and  Log in as Super User.
   
   ![Super User Login](./images/Screenshot%20from%202024-12-04%2018-13-34.png)

3. **Add data to the Tables**:

   Please Run migrations one more time.
   ```bash
   docker exec -it inventory_management-web-1 python manage.py makemigrations properties
   docker exec -it inventory_management-web-1 python manage.py migrate
   ```


   After logging in the admin panel you will see a interface like following-

   ![Admin Interface](./images/Screenshot%20from%202024-12-05%2009-31-33.png)

   You can see the your tables for the database. Click **Add** button to add data. In Location table you can see**Import** button to add data from external files. 
   ![CSV Import](./images/Screenshot%20from%202024-12-05%2009-36-04.png)

   Data Formats for the Tables

  
   ### Location

   Represents geographic locations with hierarchical nesting.

   | Field          | Type               | Description                                                                                 | Constraints                |
   |-----------------|--------------------|---------------------------------------------------------------------------------------------|----------------------------|
   | `id`           | `CharField`        | Unique identifier for the location (max 20 characters).                                     | Primary key               |
   | `title`        | `CharField`        | Name of the location (max 100 characters).                                                  | Required                  |
   | `center`       | `PointField`       | Geolocation of the location (latitude, longitude).                                          | Required                  |
   | `parent_id`    | `ForeignKey`       | Parent location for hierarchical nesting. References `Location`.                           | Nullable, Optional        |
   | `location_type`| `CharField`        | Type of location (e.g., continent, country, state, city).                                   | Default: `city`           |
   | `country_code` | `CharField`        | ISO country code (max 2 characters).                                                       | Optional                  |
   | `state_abbr`   | `CharField`        | State abbreviation (max 3 characters).                                                     | Optional                  |
   | `city`         | `CharField`        | City name (max 30 characters).                                                             | Optional                  |
   | `created_at`   | `DateTimeField`    | Timestamp when the location was created.                                                   | Auto-generated            |
   | `updated_at`   | `DateTimeField`    | Timestamp when the location was last updated.                                              | Auto-generated            |

   ### Example:
   ```json
   {
   "id": "loc123",
   "title": "San Francisco",
   "center": "POINT(-122.4194 37.7749)",
   "parent_id": "loc001",
   "location_type": "city",
   "country_code": "US",
   "state_abbr": "CA",
   "city": "San Francisco",
   "created_at": "2024-12-01T12:00:00Z",
   "updated_at": "2024-12-01T12:00:00Z"
   }
   ```
   ### Accommodation Table

   Represents properties available for booking, including location, user association, and key features.

   | Column         | Data Type                | Description                                                                 | Constraints          |
   |-----------------|--------------------------|-----------------------------------------------------------------------------|----------------------|
   | `id`           | `CharField`             | Unique identifier for the accommodation (max 20 characters).                | Primary key          |
   | `feed`         | `PositiveSmallIntegerField` | Data source identifier.                                                    | Default: `0`         |
   | `title`        | `CharField`             | Name of the accommodation (max 100 characters).                             | Required             |
   | `country_code` | `CharField`             | ISO country code (max 2 characters).                                        | Required             |
   | `bedroom_count`| `PositiveIntegerField`  | Number of bedrooms.                                                        | Optional             |
   | `review_score` | `DecimalField`          | Average review score (max 3 digits, 1 decimal).                             | Default: `0`         |
   | `usd_rate`     | `DecimalField`          | Price in USD (max 10 digits, 2 decimals).                                   | Required             |
   | `center`       | `PointField`            | Geolocation of the property.                                                | Required             |
   | `images`       | `JSONField`             | JSON array of image URLs.                                                   | Optional             |
   | `location_id`  | `ForeignKey`            | Associated location. References `Location`.                                 | Required             |
   | `amenities`    | `JSONField`             | JSON array of amenities.                                                    | Optional             |
   | `user_id`      | `ForeignKey`            | Associated user. References `User`.                                         | Nullable             |
   | `published`    | `BooleanField`          | Indicates whether the accommodation is published.                           | Default: `False`     |
   | `created_at`   | `DateTimeField`         | Timestamp when the accommodation was created.                               | Auto-generated       |
   | `updated_at`   | `DateTimeField`         | Timestamp when the accommodation was last updated.                          | Auto-generated       |

   ### Example Data:
   ```json
   {
   "id": "acc001",
   "feed": 1,
   "title": "Luxury Villa",
   "country_code": "US",
   "bedroom_count": 4,
   "review_score": 4.5,
   "usd_rate": 250.00,
   "center": "POINT(-118.2437 34.0522)",
   "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
   "location_id": "loc123",
   "amenities": ["WiFi", "Pool", "Gym"],
   "user_id": 1,
   "published": true,
   "created_at": "2024-12-01T12:00:00Z",
   "updated_at": "2024-12-01T12:00:00Z"
   }
   ```
   ### Localized Accommodation Table

   Represents localized data for accommodations, allowing descriptions and policies to be available in multiple languages.

   ### Table Structure

   | Column         | Data Type    | Description                                                       | Constraints                     |
   |-----------------|-------------|-------------------------------------------------------------------|---------------------------------|
   | `id`           | `AutoField` | Unique identifier for the localized entry.                        | Primary key                    |
   | `property_id`  | `ForeignKey`| Associated accommodation. References the `Accommodation` table.   | Required                       |
   | `language`     | `CharField` | Language code for localization (2 characters).                    | Choices: `en`, `es`, `fr`, etc.|
   | `description`  | `TextField` | Localized description of the accommodation.                       | Required                       |
   | `policy`       | `JSONField` | JSON object representing property policies in the specific language. | Required                       |

   ### Example Data

   Here’s an example JSON representation of a `Localized Accommodation` entry:

   ```json
   {
   "id": 1,
   "property_id": "acc001",
   "language": "en",
   "description": "A luxurious villa with stunning views and modern amenities.",
   "policy": {
      "check_in": "14:00",
      "check_out": "11:00",
      "cancellation": "Free cancellation up to 48 hours before check-in."
   }
   }
   ```
4. **Register a New User**:

   In Django Admin Panel Create a new user group called ***Property Owners*** and give create, change and view permissions for ***Accomodation*** Table.
   ![property-owners](./images/Screenshot%20from%202024-12-05%2010-21-48.png)

   Now Go to your Django Appliction Running on http://localhost:8000 and click Sign Up. You will be rendered with the sign up page. Now Register a new user with providing required informations.
   ![Register](./images/Screenshot%20from%202024-12-05%2010-34-43.png) 

   Now Go to your Django Admin Pannel and you will see the user. Click Highlighted Id, and make the user active and staff.
   ![is_active](./images/Screenshot%20from%202024-12-05%2010-35-51.png)
   Now you can Login and add Accomodation as Property Owner.

5. **Login**:

   You can Login from admin panel or frontend. After registering New User, The Login page will be redirected.
   ![Login](./images/Screenshot%20from%202024-12-05%2010-38-50.png)
   Give necessary informations and Login. Now navigate to https://localhost:8000/admin and You are all good to add your own Property.
   ![Admin Login](./images/Screenshot%20from%202024-12-05%2010-46-16.png)
---

## Testing


   Go to terminal and run the command
   ```bash
   docker exec -it inventory_management-web-1 bash 
   coverage run manage.py test properties
   coverage report
   ```

## Command Line Ulitility

Generate a sitemap:

```bash
docker exec -it inventory_management-web-1 python manage.py generate_sitemap
```
---
The output will be saved as sitemap.json in the root directory.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.
