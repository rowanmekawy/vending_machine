# vending machine
 APIs project for a vending machine, allowing users with a “seller” role to add, update or remove products, while users with a “buyer” role can deposit coins into the machine and make purchases. Your vending machine should only accept 5, 10, 20, 50 and 100 cent coins

## Table of Contents

- [Service-Oriented Architecture (SOA)](#service-oriented-architecture-soa)
- [Technologies Used](#technologies-used)
- [Installation](#installation)

## Service-Oriented Architecture (SOA)

This project is built using Service-Oriented Architecture (SOA), an architectural pattern that structures the application as a collection of services. Each service is designed to perform a specific business functionality and can communicate with other services through well-defined APIs.

### Key Characteristics of SOA:

- **Modularity:** Services are independent modules, making it easier to develop, test, and deploy.
- **Loose Coupling:** Services communicate through standardized interfaces, reducing dependencies between components.
- **Reusability:** Services can be reused across different parts of the application or in other projects.

### Technologies Used

- [Django](https://www.djangoproject.com/): A high-level Python web framework.
- [Django REST Framework](https://www.django-rest-framework.org/): A powerful and flexible toolkit for building Web APIs.

## Installation
Follow these steps to set up and run the project locally.

## Prerequisites

Make sure you have the following prerequisites installed on your machine:

- [Python](https://www.python.org/) (version 3.8.10)
- [PostgreSQL](https://www.postgresql.org/) database

## Clone the Repository

```bash
git clone https://github.com/rowanmekawy/your-repo.git
cd your-repo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Update the DATABASES configuration in config/settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
## Apply Migrations
python manage.py migrate

## Run the Development Server
python manage.py runserver