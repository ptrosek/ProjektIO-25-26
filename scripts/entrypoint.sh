#!/bin/bash
set -e

# Check if migrations exist for appointment package
if [ ! -d ".venv/lib/python3.12/site-packages/appointment/migrations" ] || [ -z "$(ls -A .venv/lib/python3.12/site-packages/appointment/migrations 2>/dev/null)" ]; then
    echo "Missing migrations for 'appointment'. generating them..."
    uv run python manage.py makemigrations appointment
fi

# Run migrations
echo "Running migrations..."
uv run python manage.py migrate

# Start server
echo "Starting server..."
exec uv run python manage.py runserver 0.0.0.0:8000
