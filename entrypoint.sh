#!/bin/sh

# Postgres hazır olana qədər gözləyir
echo "DB gözlənilir..."
while ! nc -z db 5432; do
  sleep 1
done

echo "DB hazırdır. Migration edilir..."
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
