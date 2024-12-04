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

- Python 3.8+
- PostgreSQL 12+ with PostGIS extension
- Django 4.0+
- Docker (optional, for containerized database setup)

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
5. **Create Super User**:

   
   ```bash
   docker exec -it inventory_management-web-1 python manage.py createsuperuser 
   ```

   Enter valiid information about superuser and create superuser

   ![Superuser](./images/Screenshot%20from%202024-12-04%2016-55-55.png)

6. **Login to Django Admin Panel**:
  
   Navigate to the [Django Admin Panel](https://localhost:8000/admin) and  Log in as Super User.
   
   ![Super User Login](./images/Screenshot%20from%202024-12-04%2018-13-34.png)

7. **Add data to the Tables**:

   After logging in the admin panel you will see a interface like following-

   ![Admin Interface](./images/)