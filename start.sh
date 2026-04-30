#!/bin/bash
export DJANGO_SUPERUSER_PASSWORD="admin@321"

echo "Running Django migrations..."
python manage.py migrate --fake-initial 2>&1 || echo "Migrations skipped (already applied)"

echo "Creating superuser..."
python manage.py createsuperuser --username=super_admin --noinput --email=admin@example.com

echo "Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

echo "Starting Django development server on port $PORT..."
gunicorn iei_project.wsgi:application --bind


