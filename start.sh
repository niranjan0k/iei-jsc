#!/bin/bash
cd /python/iei-django

export DJANGO_SETTINGS_MODULE=iei_project.settings

echo "Running Django migrations..."
python manage.py migrate --fake-initial 2>&1 || echo "Migrations skipped (already applied)"

echo "Collecting static files..."
python manage.py collectstatic --noinput 2>/dev/null || true

echo "Starting Django development server on port $PORT..."
exec python manage.py runserver 0.0.0.0:${PORT:-18985}
