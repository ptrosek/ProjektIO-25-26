# Core Fitness App

A Django-based fitness application designed to manage user memberships and schedule classes and appointments.

## Features

*   **Membership Management**: Track user memberships with statuses (Pending, Active, Rejected).
*   **Appointment Scheduling**: Integrated with `django-appointment` for managing services and appointments.
*   **Class Registration**: Users can register for specific class instances.
*   **Authentication**: Standard Django authentication with user models.

## Tech Stack

*   **Language**: Python 3.12+
*   **Framework**: Django 5.x
*   **Database**: SQLite (Default), PostgreSQL (Supported via `psycopg2-binary`)
*   **Dependency Management**: `uv`
*   **Containerization**: Docker & Docker Compose

## Prerequisites

*   [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) (Recommended)
*   OR Python 3.12+ and [uv](https://github.com/astral-sh/uv)

## Getting Started

### Using Docker (Recommended)

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Build and start the services:**
    ```bash
    docker-compose up --build
    ```
    This will build the image, install dependencies, run migrations, and start the development server.

3.  **Access the application:**
    Open your browser and navigate to `http://localhost:8000`.

### Local Development

1.  **Install `uv`:**
    If you don't have `uv` installed, follow the [official installation guide](https://github.com/astral-sh/uv).

2.  **Install dependencies:**
    ```bash
    uv sync
    ```

3.  **Apply database migrations:**
    ```bash
    uv run python manage.py migrate
    ```

4.  **Run the development server:**
    ```bash
    uv run python manage.py runserver
    ```

5.  **Access the application:**
    Open your browser and navigate to `http://localhost:8000`.

## Project Structure

*   `core_fitness`: Handles core fitness logic, including class registrations and integration with `django-appointment`.
*   `memberships`: Manages user membership details and status.
*   `config`: Django project configuration (`settings.py`, `urls.py`, etc.).
*   `scripts`: Utility scripts (e.g., `entrypoint.sh` for Docker).
*   `main.py`: A simple entry point script (primarily for testing environment setup).

## Usage

### Admin Interface
To access the admin interface, you first need to create a superuser.

**Docker:**
```bash
docker-compose exec web uv run python manage.py createsuperuser
```

**Local:**
```bash
uv run python manage.py createsuperuser
```

Then navigate to `http://localhost:8000/admin` and log in.

### Configuration
Key settings are located in `config/settings.py`.
*   **Databases**: Configured to use `db.sqlite3` by default.
*   **Appointment Config**: Custom settings for `django-appointment` can be found in `APPOINTMENT_CONFIG`.

