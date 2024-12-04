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
```bash
   cd inventory_management
   docker-compose up --build
```
