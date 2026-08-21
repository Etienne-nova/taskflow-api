#!/bin/sh
set -e

# Collecte des fichiers statiques pour Nginx
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Exécution des migrations
echo "Exécution des migrations..."
python manage.py migrate --noinput

# Exécution de la commande passée dans le docker-compose (ex: gunicorn, celery...)
exec "$@"
