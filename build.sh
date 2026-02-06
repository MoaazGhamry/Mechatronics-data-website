#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Loading initial data..."
python manage.py loaddata initial_data.json || echo "Warning: Failed to load initial_data.json"

echo "Creating superuser (if not exists)..."
# Optional: Script to auto-create superuser using env vars if needed, 
# but for now let's focus on the data load.
# We can add a custom command or script for superuser creation later if needed without shell.

echo "Build completed successfully!"
